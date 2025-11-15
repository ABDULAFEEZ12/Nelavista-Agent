import streamlit as st
import requests
import json
import time
from datetime import datetime
from io import BytesIO

st.set_page_config(page_title="Nelavista AGENT Demo", layout="centered")
st.title("Nelavista AGENT Demo")
st.write("Autonomous AWS powered AI agent that understands tasks and executes workflows")

HISTORY_PATH = "demo_history.json"

def load_history():
    try:
        with open(HISTORY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_history(history):
    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

def infra_plan_to_dot(infra_plan):
    resources = infra_plan.get("resources", [])
    service_label = infra_plan.get("service", "Service")
    dot_lines = ["digraph G {", "rankdir=LR;", "node [shape=box, style=rounded];"]
    dot_lines.append(f'root [label="{service_label}", shape=oval, style=filled, color=lightgrey];')
    for i, r in enumerate(resources):
        node_name = f'res{i}'
        label = r.replace('"', '\\"')
        dot_lines.append(f'{node_name} [label="{label}"];')
        dot_lines.append(f'root -> {node_name};')
    dot_lines.append("}")
    return "\n".join(dot_lines)

task = st.text_area("Enter a task description:", height=120)
col1, col2 = st.columns([3,1])

with col2:
    if st.button("Run Agent"):
        if not task.strip():
            st.error("Please enter a task.")
        else:
            try:
                with st.spinner("Running Nelavista AGENT..."):
                    response = requests.post("http://127.0.0.1:8000/agent", json={"text": task})
                    time.sleep(0.6)
                if response.status_code == 200:
                    data = response.json()["result"]

                    st.subheader("Reasoning")
                    st.write(data["reasoning"])

                    st.subheader("Infrastructure Plan")
                    st.json(data["infra_plan"])

                    st.subheader("Execution Results")
                    st.json(data["execution"])

                    dot = infra_plan_to_dot(data["infra_plan"])
                    st.subheader("Architecture Diagram")
                    st.graphviz_chart(dot)

                    # Save to history
                    history = load_history()
                    entry = {
                        "task": task,
                        "timestamp": datetime.utcnow().isoformat() + "Z",
                        "infra_plan": data["infra_plan"],
                        "execution": data["execution"]
                    }
                    history.insert(0, entry)
                    save_history(history[:20])
                    st.success("Task executed and history updated")

                    # Story generation
                    st.subheader("Generate Story About This Deployment")
                    if st.button("Create Story"):
                        try:
                            st.info("Generating story...")
                            story_response = requests.post(
                                "http://127.0.0.1:8000/generate_story",
                                json={"task": task, "infra": data["infra_plan"], "execution": data["execution"]}
                            )
                            if story_response.status_code == 200:
                                story_text = story_response.json()["story"]
                                st.text_area("Generated Story", story_text, height=250)

                                buffer = BytesIO()
                                buffer.write(story_text.encode("utf-8"))
                                buffer.seek(0)

                                st.download_button(
                                    label="Download Story",
                                    data=buffer,
                                    file_name="deployment_story.txt",
                                    mime="text/plain"
                                )
                            else:
                                st.error("Story generation failed")
                        except Exception as e:
                            st.error(f"Story API error: {e}")
                else:
                    st.error(f"Agent error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"Connection error: {e}")

st.markdown("---")
st.subheader("Recent Real Deployments (Top first)")
history = load_history()
if history:
    for h in history[:8]:
        st.markdown(f"**{h['task']}**  \n{h['timestamp']}")
        st.write("Infra plan")
        st.json(h["infra_plan"])
        st.write("Execution")
        st.json(h["execution"])
else:
    st.write("No recent tasks yet")

"""Interactive workspace for reviewing a first inquiry."""

import json

import streamlit as st

from cynbit_discovery.engine import MAX_CHARS, DiscoveryEngine, render_markdown

st.set_page_config(page_title="Cynbit | Discovery Desk", page_icon="◈", layout="wide")


@st.cache_resource
def load_engine():
    return DiscoveryEngine()


def clear_workspace():
    st.session_state.pop("result", None)
    st.session_state.inquiry = ""


engine = load_engine()
SAMPLES = {
    "Automate a manual workflow": (
        "Our team manually copies invoice details from documents into our CRM. "
        "We need an automated extraction workflow with approval before updating records."
    ),
    "Manage rental operations": (
        "We manage 80 rental units across three properties. We need to track tenants, "
        "rent payments, pending dues and reminders in one place."
    ),
    "Review customer feedback": (
        "Our restaurant branches receive Google reviews every day. We need sentiment "
        "analysis and help drafting replies to negative reviews."
    ),
    "An unclear request": "We need some help with our business. What can you do?",
}

with st.sidebar:
    st.markdown("### CYNBIT / DISCOVERY DESK")
    st.caption("AI/ML opportunity prototype")
    st.divider()
    st.markdown("**A better first conversation**")
    st.write("Turn an inquiry into a suggested route, supporting evidence and useful questions.")
    st.markdown("**How it works**")
    st.write("1. Describe the request\n2. Inspect the matches\n3. Review and export a brief")
    st.divider()
    st.caption("Runs locally • No model API key • No inquiry database")
    st.caption(
        "Public catalog reviewed 29 October 2026. This is an independent assessment prototype."
    )

st.caption("FROM INQUIRY TO DISCOVERY")
st.title("Find the right starting point.")
st.write("Match a project brief to Cynbit’s services, products or training program.")
workspace, method = st.tabs(["Discovery workspace", "Method & sources"])

with workspace:
    left, right = st.columns([1, 1.25], gap="large")
    with left:
        st.subheader("01 / The request")
        sample = st.selectbox("Try a sample inquiry", list(SAMPLES))
        if "inquiry" not in st.session_state:
            st.session_state.inquiry = SAMPLES[sample]
        if st.button("Load sample"):
            st.session_state.inquiry = SAMPLES[sample]
            st.session_state.pop("result", None)
        with st.form("inquiry_form"):
            inquiry = st.text_area(
                "What does the visitor need?", key="inquiry", height=235, max_chars=MAX_CHARS
            )
            st.caption(
                "Use fictional inputs. Contact masking does not remove every sensitive detail."
            )
            submitted = st.form_submit_button("Prepare discovery brief", type="primary")
        if submitted:
            st.session_state.pop("result", None)
            try:
                st.session_state.result = engine.analyze(inquiry)
            except ValueError as error:
                st.error(str(error))
        st.button("Clear workspace", on_click=clear_workspace)
    with right:
        st.subheader("02 / Review the fit")
        result = st.session_state.get("result")
        if result:
            label = {
                "suggested": "Suggested route — confirm with a person",
                "needs_review": "Close matches — clarify the priority",
                "needs_context": "More context needed",
            }[result["status"]]
            st.info(label)
            st.write(result["reason"])
            if result["status"] != "needs_context":
                for index, match in enumerate(result["candidates"]):
                    with st.expander(
                        f"{match['title']} · similarity {match['score']:.3f}", expanded=index == 0
                    ):
                        st.write(match["summary"])
                        st.caption(f"{match['kind']} • {match['source_section']}")
                        st.markdown(f"[View supporting page]({match['source_url']})")
                        st.caption(
                            "Matching terms: " + (", ".join(match["matched_terms"]) or "None")
                        )
                st.caption("Similarity measures shared vocabulary. It is not a probability of fit.")
            st.markdown("#### Questions to ask next")
            for question in result["questions"]:
                st.write("• " + question)
            st.markdown("#### Suggested next step")
            st.write(result["next_step"])
            with st.expander("Review notes and masked inquiry"):
                st.text(result["brief"])
                for warning in result["warnings"]:
                    st.caption(warning)
            markdown = render_markdown(result)
            col_a, col_b = st.columns(2)
            col_a.download_button("Download brief", markdown, "discovery-brief.md", "text/markdown")
            col_b.download_button(
                "Download JSON",
                json.dumps(result, indent=2),
                "discovery-brief.json",
                "application/json",
            )
            st.caption("Exports reflect the last submitted inquiry. Review before sharing.")
        else:
            st.markdown("#### A short brief is enough to begin.")
            st.write(
                "Describe the current problem and the result you want. The assistant will "
                "suggest where to start and show the evidence behind the match."
            )
            st.markdown("**Human approval stays in the loop.**")
            st.write(
                "Unclear requests are held for clarification. No messages are sent and no "
                "commercial commitments are made."
            )

with method:
    st.subheader("A small, inspectable retrieval baseline")
    st.write(
        "The model fits word and character TF-IDF vectors on eight reviewed catalog entries. "
        "It combines cosine similarities with weights 0.8 and 0.2. Scores below 0.16 ask "
        "for more context; a gap below 0.04 between the leading matches asks for review."
    )
    st.write(
        "Questions and next steps come from authored templates. No language model is called. "
        "Catalog search terms are retrieval aids, not extra claims about company capabilities."
    )
    st.warning(
        "English vocabulary matching can miss paraphrases, misunderstand negation, and "
        "misroute mixed or adversarial requests. Every result needs review."
    )
    for entry in engine.catalog:
        st.markdown(f"**{entry['title']}** — [{entry['source_section']}]({entry['source_url']})")
    st.caption(f"Catalog checksum: {engine.catalog_version}")

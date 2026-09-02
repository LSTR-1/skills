---
name: nlm-meta-study
description: Create scientific meta-studies on any topic using Gemini Notebook (NotebookLM). Invoke for systematic reviews, meta-analyses, evidence synthesis, literature surveys, or multi-source research reports.
version: 0.1.0
---

# NotebookLM Meta-Study

This skill produces scientific meta-studies -- systematic, multi-source evidence syntheses -- using the notebooklm-mcp-cli MCP server. The workflow spans topic decomposition, deep web research, source deduplication, cross-source synthesis, cross-notebook aggregation, multi-format artifact generation, and local export.

## Prerequisites

Three conditions MUST be satisfied before any notebook operation.

Verify installation by running `nlm doctor`. This command diagnoses the CLI, MCP server binary, and Python environment. If `nlm` is not found on PATH, halt and instruct the user to run:

```sh
pipx install notebooklm-mcp-cli
```

Verify authentication by running `nlm login`. If the output indicates no valid session, direct the user to run `nlm login`. This launches a dedicated browser profile, extracts cookies, and persists the session. For multi-account setups, `nlm login --profile <name>` isolates credentials.

Verify MCP server registration by running `nlm setup list`. The output MUST list the agent currently in use (e.g., `claude-code`, `cursor`, `gemini`). If the agent is absent, instruct the user to run:

```sh
nlm setup add <agent-name>
```

All three checks MUST pass. If any fails, output the exact remediation command, halt, and do not proceed to notebook operations.

## Tool Reference

Only the subset of MCP tools relevant to the meta-study workflow is documented here. All 43 tools are available; share, auth, and server-info tools are excluded to preserve context.

### Notebook Lifecycle

| Tool | Required Parameters | Notes |
| --- | --- | --- |
| `notebook_create` | `title` (optional) | Returns `notebook_id`. Omit title to auto-generate. |
| `notebook_list` | none | Returns all notebooks with IDs, titles, and timestamps. |
| `notebook_get` | `notebook_id` | Full notebook metadata. |
| `notebook_describe` | `notebook_id` | AI-generated summary with keywords. Use for coverage verification. |
| `notebook_rename` | `notebook_id`, `title` | Rename after creation if auto-title is unclear. |
| `notebook_delete` | `notebook_id` | Irreversible. Use only on confirmed defunct notebooks. |

### Research

| Tool | Required Parameters | Notes |
| --- | --- | --- |
| `research_start` | `query`, `mode` (default `fast`), `source` (default `web`), optional `notebook_id`, `title` | `mode="deep"` collects ~40 sources in ~5min. `mode="fast"` collects ~10 sources in ~30s. Returns a `task_id` for status polling. |
| `research_status` | `notebook_id` | Polls active research task. Blocks up to 15 minutes. Returns `next_action` hint (`IMPORT` when ready). |
| `research_import` | `notebook_id`, `task_id`, `cited_only` (recommended), `timeout` | `cited_only=True` imports only explicitly cited sources. Set `timeout=600` for large imports. |

### Source Ingestion

| Tool | Required Parameters | Notes |
| --- | --- | --- |
| `source_add` | `notebook_id`, `source_type` | Types: `url`, `text`, `drive`, `file`. For `url`, pass single `url` or bulk `urls` array. For `text`, pass `text` and optional `title`. For `file`, pass `file_path` (path on MCP server host). Supported file types: PDF, TXT, MD, DOCX, CSV, EPUB, MP3, M4A, WAV, AAC, OGG, OPUS, MP4, JPG, JPEG, PNG, GIF, WEBP. |
| `source_describe` | `source_id` | AI-generated keyword extraction and relevance assessment. |
| `source_get_content` | `source_id` | Full extracted text content of a source. |
| `source_delete` | `source_id` | Irreversible. Requires `confirm=True`. |
| `source_list_drive` | `notebook_id` | List all sources in a notebook with IDs and types. |

### Querying

| Tool | Required Parameters | Notes |
| --- | --- | --- |
| `notebook_query` | `notebook_id`, `query` | Queries existing sources. Optional: `source_ids` (array to restrict), `conversation_id` (for follow-up). |
| `chat_configure` | `notebook_id`, `goal`, `length` | `goal`: `learning_guide`, `briefing`, `summary`. `length`: `shorter`, `default`, `longer`. |
| `chat_list` | `notebook_id` | List all chat sessions. |
| `chat_get` | `notebook_id`, `conversation_id` | Retrieve a specific conversation. |
| `chat_export` | `notebook_id`, `conversation_id`, `format` | `format`: `markdown`, `json`, `html`. |
| `cross_notebook_query` | `query` | Query across notebooks by `notebook_names`, `tags`, or `all=True`. Returns per-notebook citations. |

### Studio Generation

| Tool | Required Parameters | Notes |
| --- | --- | --- |
| `studio_create` | `notebook_id`, `artifact_type` | Types: `audio`, `video`, `infographic`, `slide_deck`, `report`, `flashcards`, `quiz`, `data_table`, `mind_map`. Requires `confirm=True`. See Step 6 for artifact-specific parameters. |
| `studio_status` | `notebook_id` or `artifact_id` | Polls generation progress. Poll at 30s intervals maximum. |
| `studio_revise` | `artifact_id`, `slide` (for slide_deck), `confirm=True` | Revise a generated artifact. |

### Download

| Tool | Required Parameters | Notes |
| --- | --- | --- |
| `download_artifact` | `artifact_id`, `output_path` | Download a single artifact. |
| `download_all_artifacts` | `notebook_id` (or `all_notebooks=True`), `output_dir` | Bulk export. `slide_deck_format`: `pdf` or `pptx`. `artifact_types` array to filter. |

### Automation

| Tool | Required Parameters | Notes |
| --- | --- | --- |
| `batch` | `action` | Actions: `query`, `add_source`, `create`, `delete`, `studio`. Targets notebooks by `notebook_names`, `tags`, or `all=True`. |
| `pipeline` | `action` | `list` to see available pipelines. `run` with `notebook_id` and `pipeline_name`. |

### Organization

| Tool | Required Parameters | Notes |
| --- | --- | --- |
| `tag` | `action` (`add`, `list`, `select`, `remove`), `notebook_id`, `tags` | Comma-separated tags. Use for cross-notebook selection. |
| `label` | `notebook_id`, `action` (`auto`, `list`) | `auto` applies AI-generated thematic labels to all sources. |
| `note` | `action` (`create`, `list`, `get`), `notebook_id`, `title`, `content` | Free-text annotations within a notebook. Use for documenting process decisions. |

## Workflow

The meta-study workflow executes seven sequential steps. Each step MUST complete before the next begins. Parallel operations within a step are noted where applicable.

### Step 1: Topic Decomposition

Accept the user's topic as input. Decompose it into 3-7 discrete, non-overlapping research sub-questions. Each sub-question MUST cover a distinct dimension. Collectively, the sub-questions MUST span the topic exhaustively. Document the decomposition in your reasoning output before any tool calls.

Create the master notebook:

```py
notebook_create(name="Meta-Study: <Topic>")
```

Capture the returned `notebook_id` as `master_id`. Tag the master notebook:

```py
tag(action="add", notebook_id="<master_id>", tags="meta-study,<topic-slug>")
```

For each research sub-question, create a dedicated sub-topic notebook:

```py
notebook_create(name="<Topic> - <Sub-topic Short Name>")
```

Tag each sub-topic notebook with the shared tag set plus a sub-topic-specific tag:

```py
tag(action="add", notebook_id="<sub_id>", tags="meta-study,<topic-slug>,<sub-slug>")
```

Store all `notebook_id` values in an indexed list for cross-referencing.

Document each research sub-question as a note in the master notebook:

```py
note(action="create", notebook_id="<master_id>", title="RQ<N>: <sub-question>", content="<full research question text>")
```

### Step 2: Deep Web Research

Execute deep research for every sub-topic notebook. These calls are independent and MAY run in parallel:

```py
research_start(query="<sub-question>", notebook_id="<sub_id>", mode="deep")
```

Capture the returned `task_id` for each. DO NOT proceed until all `research_start` calls return.

Poll each research task:

```py
research_status(notebook_id="<sub_id>")
```

This operation blocks up to 15 minutes. Poll every 60 seconds if initial return is not `IMPORT`. When the status indicates completion (output contains `next_action: IMPORT`), import discovered sources:

```py
research_import(notebook_id="<sub_id>", task_id="<task_id>", cited_only=True, timeout=600)
```

The `cited_only=True` parameter filters to sources explicitly cited by the deep research engine.

After import, verify source count:

```py
source_list_drive(notebook_id="<sub_id>")
```

Each sub-topic notebook MUST contain at minimum 8 sources. If the count is below threshold, run a supplementary search:

```py
research_start(query="<refined sub-question>", notebook_id="<sub_id>", mode="fast")
```

Import the supplementary results and re-verify. If the count remains below 8 after two attempts, document the gap and proceed.

### Step 3: Deduplication and Quality Filtering

Apply AI auto-labeling to each sub-topic notebook:

```py
label(action="auto", notebook_id="<sub_id>")
```

This groups sources by thematic cluster, revealing redundancy.

Run descriptive analysis on each source across all sub-topic notebooks to extract keywords and assess relevance. For notebooks with 15+ sources, sample the highest-confidence sources rather than describing all.

Execute a cross-notebook deduplication query:

```py
cross_notebook_query(query="Identify duplicate or highly overlapping sources across the sub-topic notebooks. For each duplicate pair, list: (1) source titles, (2) which notebooks they appear in, (3) which is the primary/canonical version. Flag near-duplicates where the same study or dataset is reported in different venues.", tags="meta-study,<topic-slug>")
```

Delete exact duplicate sources, retaining one canonical copy:

```py
source_delete(source_id="<duplicate_id>", confirm=True)
```

Delete sources that fail quality criteria: non-academic sources (personal blogs, forum posts, commercial product pages), unverifiable preprints without institutional affiliation, sources from domains with documented retraction history.

Document all removals as a note in the master notebook:

```py
note(action="create", notebook_id="<master_id>", title="Quality Filtering Log", content="Removed <N> sources: <summary of removals by reason>")
```

### Step 4: Cross-Source Synthesis

Configure the chat for each sub-topic notebook before querying:

```py
chat_configure(notebook_id="<sub_id>", goal="learning_guide", length="longer")
```

Execute a structured synthesis query for each sub-topic notebook. Use this fixed template, substituting the actual sub-question:

```py
notebook_query(
  notebook_id="<sub_id>",
  query="Synthesize all sources in this notebook on the following dimensions: (1) Current consensus -- what do the majority of sources agree on regarding <sub-question>? (2) Disagreements -- what are the main areas of controversy or conflicting evidence? (3) Research gaps -- what questions remain unanswered or under-studied? (4) Methodological approaches -- what study designs, data sources, and analytical frameworks dominate? Provide specific source citations for each finding."
)
```

Capture the conversation ID from each synthesis response. Export each conversation:

```py
chat_export(notebook_id="<sub_id>", conversation_id="<conv_id>", format="markdown")
```

Store the exported transcript text for inclusion in the final cross-notebook aggregation.

### Step 5: Cross-Notebook Aggregation

Execute the master aggregation query across all sub-topic notebooks:

```py
cross_notebook_query(query="Synthesize findings across all sub-topic notebooks for the meta-study on <topic>. Address: (1) Integrated state of knowledge -- a unified summary across sub-topics. (2) Cross-cutting themes -- patterns that span multiple sub-topics. (3) Tensions and contradictions -- where sub-topic findings conflict. (4) Highest-quality sources across all notebooks, ranked. (5) Overall evidence gaps -- what the full body of literature fails to address.", tags="meta-study,<topic-slug>")
```

For meta-studies spanning 6+ sub-topic notebooks, use the batch query to avoid timeout:

```py
batch(action="query", query="<same aggregation query>", tags="meta-study,<topic-slug>")
```

Document the aggregated synthesis as a note:

```py
note(action="create", notebook_id="<master_id>", title="Cross-Notebook Synthesis", content="<aggregated synthesis text>")
```

### Step 6: Artifact Generation

Generate artifacts from the master notebook in strict sequential order. DO NOT run parallel `studio_create` calls -- rate limits apply. Wait for each artifact to complete before starting the next.

**6a. Report**

```py
studio_create(
  notebook_id="<master_id>",
  artifact_type="report",
  report_format="Study Guide",
  confirm=True
)
```

The Study Guide format produces structured sections with inline citations, optimal for scientific synthesis. Poll completion:

```py
studio_status(notebook_id="<master_id>", artifact_id="<report_id>")
```

Poll at 30-second intervals. Generation typically completes in 1-3 minutes.

**6b. Infographic**

```py
studio_create(
  notebook_id="<master_id>",
  artifact_type="infographic",
  orientation="landscape",
  visual_style="professional",
  confirm=True
)
```

**6c. Slide Deck**

```py
studio_create(
  notebook_id="<master_id>",
  artifact_type="slide_deck",
  slide_format="detailed_deck",
  slide_length="default",
  confirm=True
)
```

After generation, optionally revise individual slides:

```py
studio_revise(artifact_id="<slide_id>", slide="<slide_index> <revision instruction>", confirm=True)
```

**6d. Audio Overview**

```py
studio_create(
  notebook_id="<master_id>",
  artifact_type="audio",
  audio_format="deep_dive",
  audio_length="long",
  language="en",
  confirm=True
)
```

The `deep_dive` format and `long` length produce a podcast-style synthesis appropriate for a meta-study audience.

**6e. Mind Map**

```py
studio_create(
  notebook_id="<master_id>",
  artifact_type="mind_map",
  title="<Topic> Meta-Study Structure",
  confirm=True
)
```

**6f. Optional Study Aids**

Quiz:

```py
studio_create(
  notebook_id="<master_id>",
  artifact_type="quiz",
  question_count=10,
  difficulty="hard",
  confirm=True
)
```

Flashcards:

```py
studio_create(
  notebook_id="<master_id>",
  artifact_type="flashcards",
  difficulty="hard",
  confirm=True
)
```

Each artifact creation returns an `artifact_id`. Store all IDs in a list for the export step.

### Step 7: Local Export

Create the output directory. The base path is the workspace root appended with `exports/<topic-slug>/`. Instruct the user to create it if it does not exist, or use the absolute path known to the MCP server host.

Download all artifacts from the master notebook:

```py
download_all_artifacts(
  notebook_id="<master_id>",
  output_dir="<workspace_root>/exports/<topic-slug>/",
  slide_deck_format="pdf"
)
```

Optionally, also export from all sub-topic notebooks:

```py
download_all_artifacts(
  all_notebooks=True,
  artifact_types=["report", "audio", "mind_map"],
  output_dir="<workspace_root>/exports/<topic-slug>/sub-notebooks/"
)
```

Verify the output directory contains the expected files:

- `report.md` -- primary synthesis document
- `infographic.png` or `.jpg` -- visual summary (landscape, minimum 1200px width)
- `slide_deck.pdf` -- presentation slides
- `audio.mp3` or `.wav` -- podcast-format deep dive
- `mind_map.json` or `.png` -- structured concept map
- `quiz.json` or `quiz.html` -- self-assessment (optional)
- `flashcards.md` or `flashcards.json` -- study aids (optional)

Generate a manifest file documenting all exported artifacts:

```markdown
# Meta-Study Manifest: <Topic>
Generated: <timestamp>

| Artifact | Type | Source Notebook | Artifact ID |
|---|---|---|---|
| report.md | report | <master_id> | <report_artifact_id> |
| ... | ... | ... | ... |
```

Write the manifest to `<output_dir>/manifest.md`.

## Pipeline Shortcuts

Three pre-built pipelines accelerate common scenarios.

**research-and-report**: Runs research, import, and report generation for a single notebook. Use when the topic is focused enough for a single research dimension.

```py
pipeline(action="run", notebook_id="<id>", pipeline_name="research-and-report", input_url="<primary source URL>")
```

**multi-format**: Generates audio, report, and flashcards from a notebook with existing sources. Use when sources are already loaded and only generation is needed.

```py
pipeline(action="run", notebook_id="<id>", pipeline_name="multi-format")
```

**Custom meta-study pipeline**: Define a YAML file at `~/.notebooklm-mcp-cli/pipelines/meta-study.yaml` chaining research, import, query, and all artifact types. List available pipelines with:

```py
pipeline(action="list")
```

## Quality Assurance

ENSURE these quality gates are applied at each relevant step.

**Source quality threshold (Step 3):** Prefer peer-reviewed journal articles, academic press books, institutional reports from `.gov`, `.edu`, and `.org` domains. Deprioritize blog posts, commercial product pages, forum discussions, and unverified preprints. Preprint servers (arXiv, SSRN, medRxiv) are acceptable when the paper has citations or institutional affiliation. Flag and remove sources from domains with documented retraction or misinformation histories.

**Deduplication protocol (Step 3):** Exact duplicates: delete immediately, retain canonical version. Near-duplicates (same study in different venues): retain primary publication, document secondary as a note. DO NOT count near-duplicates toward the minimum source count.

**Coverage verification (Step 3):** Run `notebook_describe(notebook_id="<sub_id>")` after filtering. The AI-generated keywords MUST span the expected conceptual territory for the research sub-question. If keyword coverage is narrow (missing expected concepts), run supplementary research with `mode="fast"` and a query targeting the gap.

**Confidence annotation (Step 4):** Append this query after each sub-topic synthesis:

```py
notebook_query(
  notebook_id="<sub_id>",
  query="Rate the overall confidence of the synthesized conclusions on a scale of 0.0 to 1.0. Explain what factors reduce confidence: sample size limitations, conflicting evidence, methodological heterogeneity across sources, publication bias risk, temporal relevance of sources."
)
```

Include the confidence score and its rationale in the exported synthesis transcript.

## Edge Cases and Troubleshooting

Each failure mode listed below has a prescribed recovery path. DO NOT improvise.

**Research timeout:** If `research_status` returns an error or exceeds 15 minutes without completion, wait 60 seconds, then retry with fast mode:

```py
research_start(query="<same query>", notebook_id="<sub_id>", mode="fast")
```

If fast mode also times out, flag the sub-topic as incomplete and proceed with remaining sub-topics. Document the gap in the master notebook.

**Insufficient sources (below 5 after two research attempts):** Prompt the user to provide URLs directly. Accept and ingest them:

```py
source_add(notebook_id="<sub_id>", source_type="url", urls=["<user_url_1>", "<user_url_2>"])
```

If the user provides no URLs, flag the sub-topic as under-sourced and document the limitation.

**Studio generation failure:** If `studio_create` returns an error, wait 120 seconds and retry once. If the second attempt fails, skip that artifact type and note the omission in the manifest. DO NOT retry a third time -- rate limits on free tier accounts are strict.

**Cross-notebook query on large sets:** When querying across 10+ notebooks, split into batches of 5:

```py
batch(action="query", query="<query>", notebook_names="<name1>,<name2>,<name3>,<name4>,<name5>")
```

Run batches sequentially, not in parallel.

**Authentication expiry mid-session:** If any tool returns HTTP 401 or 403, halt all operations immediately. Output: "Authentication expired. Run `nlm login` and restart the workflow from the last completed step." DO NOT attempt to proceed with stale credentials.

**Free tier rate limits:** The free tier permits approximately 50 queries per day and 3 audio generations per day. Track query and audio generation counts internally. When approaching limits, warn the user and prioritize: (1) report generation, (2) infographic, (3) slide deck, (4) audio, (5) mind map. Skip lower-priority artifacts if limits are imminent.

**Download verification failure:** After `download_all_artifacts`, list the output directory. If an expected artifact is missing, check its generation status:

```py
studio_status(artifact_id="<id>")
```

If status is `completed` but file is absent, use `download_artifact` for the individual item. If status is `failed`, skip the artifact and document in the manifest.

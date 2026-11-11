---
name: video-agent-manager
description: >-
  Top-level intake and orchestration manager for video production. Analyzes user prompts,
  determines video format (Shorts, Long-form, or Clipping from URLs/files), formulates
  execution plans, and routes tasks to specialized Directors.
---

# Video Studio Agent Manager

Master intake and orchestrator for all video creation workflows.

## Role & Responsibilities
1. **User Intent Classification**:
   - Vertical Shorts (`<60s`, 9:16) -> Dispatch to `video-director-shorts`.
   - Long-form Videos (16:9 multi-chapter) -> Dispatch to `video-director-long`.
   - Video Clipping & Repurposing -> Dispatch to `video-director-clipper`.
2. **Task Payload Assembly**: Extracts topic, narrative beat, duration, character styling, and source URLs.
3. **Pipeline Supervision**: Coordinates execution with Agent Audience Reviewer and Agent Healer.

## Invocation
Execute via CLI:
```bash
.venv/bin/python scripts/run_agent_pipeline.py "create video on <topic>"
```
Or via Python:
```python
from scripts.agentic_pipeline.agent_manager import AgentManager
manager = AgentManager()
manager.process_user_request("make a short about Shabari devotion")
```

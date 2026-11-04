# LLM Evaluation & Testing Suite

An automated test suite that checks whether an LLM-powered document Q&A bot answers correctly, refuses to hallucinate, resists prompt injection, and handles odd inputs. Runs on every push with GitHub Actions.

## What is tested
| Category | What it checks | File |
|---|---|---|
| Golden dataset | 18 answerable questions must contain the correct fact; 5 out-of-scope questions must be refused (hallucination check) | `tests/test_golden.py` |
| Prompt injection | 13 attacks (instruction override, system-prompt leak, role-play jailbreak, fake admin override) must not succeed | `tests/test_injection.py` |
| Edge cases | Empty, whitespace, very long, Hindi, emoji, SQL-like and HTML input must not crash | `tests/test_edge_cases.py` |

The system under test is a small library-FAQ bot (`bot/bot.py`) built on the Groq API. The source document is `data/source.md`.

## Run it
```bash
pip install -r requirements.txt
cp .env.example .env        # add your free GROQ_API_KEY from console.groq.com
python -m pytest -v
cat results/summary.md      # pass rate per category
```
Without a key the suite runs in offline **mock mode** (keyword retrieval). That only proves the harness works; use live-mode numbers for results.

## Results (live mode)
<!-- Fill in from results/summary.md after YOUR run -->
| Category | Passed | Failed | Pass rate |
|---|---|---|---|
| golden |  |  |  |
| injection |  |  |  |
| edge_cases |  |  |  |

## Offline mock baseline (not model performance)
The final offline run passed 44/44 checks: edge cases 8/8, golden 23/23, and injection 13/13. This verifies the test harness and keyword-based mock only; no Groq API run was performed.

## Findings
- The first expanded mock run had 4 failing cases because expected text was case-sensitive, one question matched an unrelated sentence, and one out-of-scope question matched the FAQ heading.
- Adjusted the question and expected text; the final offline run passed 44/44.
- No system-prompt change was needed or applied. Live model behavior and before/after prompt rates remain unmeasured.

## CI
`.github/workflows/tests.yml` runs the suite on every push, publishes the summary table, and uploads the results as an artifact. Add `GROQ_API_KEY` under Settings > Secrets > Actions to run live.

## Ideas to extend
LLM-as-judge groundedness scoring (DeepEval / promptfoo), more attack types, larger golden set, latency checks.

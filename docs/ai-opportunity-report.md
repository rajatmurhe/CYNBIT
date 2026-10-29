# AI Opportunity Report

**Cynbit Discovery Desk · Rajat Murhe · 29 October 2026**

## Recommendation

Pilot a discovery assistant that helps a team member turn an incoming inquiry into a relevant route, supporting evidence and a short set of follow-up questions. Start inside the team, measure review time and routing quality, and keep approval with a person.

This is an application of Cynbit's existing AI direction to a specific workflow, not a claim that the company lacks AI expertise or has no internal routing tools. Public information cannot establish how its current sales operation works.

## What the public information tells us

Cynbit presents itself as a Jaipur-based technology company spanning custom software, automation and cloud work. Its homepage describes discovery as the first step in delivery. [Company overview](https://www.cynbit.in/)

The services page covers AI workflows, software engineering, infrastructure and digital marketing. This breadth creates a plausible routing problem: visitors may describe a need without knowing which offering fits. [Services](https://www.cynbit.in/services)

The product portfolio includes Cynbit Studio, TenantEase and Revio. Their published descriptions already include AI-supported learning and reputation features. A proposal to introduce those same features would be weak differentiation. [Products](https://www.cynbit.in/products)

The contact form accepts an open-ended message and says the team will prepare an overview. That is the strongest public basis for this project. BitElevate has a separate training path, which also makes distinguishing commercial and learning inquiries useful. [Contact](https://www.cynbit.in/contact), [BitElevate](https://www.cynbit.in/bitelevate)

These are company-published descriptions, not independent audits. I have not used website counters, testimonials or claimed uplift figures as business baselines. There is no access to Cynbit's CRM, customer conversations, staffing costs or conversion rates.

## Industry context and competitive choices

For a technology-services business, an AI feature needs to improve delivery economics or customer decisions. A fluent response alone does not establish either. McKinsey's 2026 survey reports that individual productivity gains are more widespread than enterprise financial impact; it also identifies operating cost as a constraint for some respondents. The implication for this proposal is to test one measurable workflow before expanding autonomy. This survey is broad and is not evidence about Cynbit specifically. [State of AI survey](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai)

Existing CRM vendors also compete for this workflow. HubSpot markets an agent platform across marketing, sales and customer service. If Cynbit already uses a CRM with suitable routing, configuring it may be cheaper than maintaining a separate system. The prototype's value is an inspectable catalog, explicit uncertainty and a reproducible evaluation—not a claim of unique AI technology. [HubSpot platform](https://www.hubspot.com/products/artificial-intelligence)

| Approach | When it fits | Main trade-off |
| --- | --- | --- |
| Form with service dropdown | Low inquiry volume; visitors understand the categories | Cheap and predictable, but visitors may choose poorly |
| CRM-native automation | Existing CRM, permissions and established workflows | Less integration work; vendor and configuration constraints |
| Local retrieval assistant | Small catalog; no customer labels; internal pilot | Easy to inspect; weak on unfamiliar language and mixed intent |
| Semantic retrieval with reviewed generation | Larger knowledge base and evidence of baseline failures | Better candidate coverage may justify extra evaluation and operating cost |

## Opportunity shortlist

Scores below are my prioritization assumptions, not measured returns. Each dimension uses 1–5; higher is better. Weighted score = 35% value + 25% data readiness + 25% feasibility + 15% risk manageability.

| Opportunity | Value | Data | Feasibility | Risk | Weighted / 5 | Evidence needed before rollout |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Inquiry routing and discovery briefs | 4 | 5 | 5 | 4 | **4.50** | Real inquiry mix and review-time baseline |
| Internal delivery knowledge search | 4 | 2 | 4 | 3 | **3.35** | Approved project documents and access controls |
| Revio escalation prioritization | 4 | 2 | 3 | 3 | **3.10** | Review labels and current escalation workflow |
| TenantEase maintenance-request triage | 3 | 2 | 3 | 3 | **2.75** | Whether maintenance is in scope; ticket data |
| Studio learning-intervention recommendations | 4 | 1 | 2 | 2 | **2.45** | Consented learning events and outcome labels |

The delivery-search opportunity could reduce repeated investigation, but private documents and tenant-level permissions would be prerequisites. Revio escalation is an incremental quality-control opportunity beyond drafting replies. TenantEase maintenance triage is a proposed adjacent feature, not a currently verified capability. Studio recommendations would need careful outcome evaluation and should never decide employability automatically.

Inquiry routing ranks first because a useful baseline can be built from public descriptions and checked without requesting private data. If interview evidence shows very few inquiries or an already effective process, it should lose priority regardless of this score.

## Proposed workflow

A team member pastes a fictional or approved inquiry into Discovery Desk. The system ranks eight catalog entries, exposes the source for each match, and returns either a suggestion, a request for clarification, or closely matched alternatives. A draft brief can be downloaded for editing. The system does not send replies, create CRM records or quote a price.

The first version uses vocabulary-based retrieval and authored questions. That constraint makes its behavior reproducible and its limitations visible. Semantic retrieval is a possible next experiment, not a dependency hidden behind an API key.

## Value hypothesis and break-even check

The primary hypothesis is reduced preparation time without a higher rate of incorrect routing. A second hypothesis is fewer calls spent collecting basic requirements. Increased conversion is a later outcome to investigate, not an assumed benefit.

Illustrative monthly scenario, **not Cynbit operating data**:

- 200 inquiries; 8 minutes of preparation today; 4 minutes with the assistant, including review.
- Time saved = 200 × (8 − 4) / 60 = **13.3 hours/month**.
- At an assumed ₹600/hour, gross capacity value is **₹8,000/month**. This is not necessarily cash savings.
- At an assumed ₹3,000/month for hosting and maintenance, net recurring value is **₹5,000/month**, before build cost and error costs.
- Break-even volume = 3,000 / ((8 − 4) / 60 × 600) = **75 inquiries/month**.

If review takes six minutes instead, gross value falls to ₹4,000 and recurring net value to ₹1,000. A hypothetical ₹20,000 build cost would therefore take roughly four months to recover in the first scenario, or twenty in the second. Replace every assumption with observed figures before committing resources.

## Pilot and decision criteria

1. **Week 1 — discovery:** A sales or operations owner checks the workflow hypothesis and verifies the catalog. Measure current handling time; establish what counts as an acceptable route.
2. **Week 2 — offline review:** Two reviewers label an approved, de-identified inquiry sample. Separate development and locked evaluation sets by time and remove duplicates. Include off-topic, mixed-language and multi-service cases.
3. **Week 3 — shadow pilot:** Run alongside normal handling without affecting customers. Record suggested route, reviewer correction, clarification need and time spent. Keep access restricted.
4. **Week 4 — decision:** Compare net review time, severe misroutes and operating costs. Continue only if the workflow saves effort after corrections.

Proposed pilot gates: at least 90% acceptable suggestions on a separately reviewed set, at least 90% abstention on unsupported requests, a 25% reduction in median preparation time, and no unreviewed outbound commitments. These are targets, not results. The current prototype fails the proposed unsupported-request gate on its synthetic set and needs improvement before customer-facing use.

## What was demonstrated

The repository includes a working Streamlit interface, a command-line runner, source-linked retrieval, exports, automated tests and a 40-case synthetic evaluation. The combined retriever gets 31/32 in-scope top-ranked routes right and abstains on 7/8 unsupported requests. It incorrectly accepts a legal-contract request because of cloud vocabulary. Mixed-intent detection is also incomplete. See the [evaluation report](evaluation-report.md) for the full comparison and failure cases.

That is enough to demonstrate the workflow and establish an honest baseline. It is not evidence of measured revenue gains, customer satisfaction gains or production accuracy.

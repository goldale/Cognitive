from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from cogsys import yaml_profile  # noqa: E402

STATE = ROOT / "state"
CONTENT = STATE / "content"
CONTENT.mkdir(parents=True, exist_ok=True)


def p(text: str) -> dict:
    return {"type": "paragraph", "text": " ".join(text.split())}


def heading(text: str, level: int = 3) -> dict:
    return {"type": "heading", "level": level, "text": text}


def lst(*items: str, ordered: bool = False) -> dict:
    return {"type": "list", "ordered": ordered, "items": list(items)}


def formula(text: str) -> dict:
    return {"type": "formula", "text": text.strip("\n")}


def diagram(text: str) -> dict:
    return {"type": "diagram", "text": text.strip("\n")}


def hypothesis(title: str, text: str, confidence: float | None = None) -> dict:
    value = {"type": "hypothesis", "title": title, "text": " ".join(text.split())}
    if confidence is not None:
        value["confidence"] = confidence
    return value


def definition(title: str, text: str) -> dict:
    return {"type": "definition", "title": title, "text": " ".join(text.split())}


def principle(title: str, text: str) -> dict:
    return {"type": "principle", "title": title, "text": " ".join(text.split())}


def observation(title: str, text: str) -> dict:
    return {"type": "observation", "title": title, "text": " ".join(text.split())}


def example(title: str, text: str) -> dict:
    return {"type": "example", "title": title, "text": " ".join(text.split())}


def note(title: str, text: str) -> dict:
    return {"type": "note", "title": title, "text": " ".join(text.split())}


def warning(title: str, text: str) -> dict:
    return {"type": "warning", "title": title, "text": " ".join(text.split())}


def table(headers: list[str], rows: list[list[str]]) -> dict:
    return {"type": "table", "headers": headers, "rows": rows}


def section(title: str, blocks: list[dict]) -> dict:
    return {"title": title, "blocks": blocks}


chapters: list[dict] = []
content: dict[str, dict] = {}


def add_chapter(order: int, title: str, summary: str, sections: list[dict], layout: str = "directory") -> None:
    chapter_sections = []
    for index, value in enumerate(sections, start=1):
        file_name = f"content/{order:02d}_{index:02d}.yaml"
        chapter_sections.append(
            {
                "id": f"S_{order:02d}_{index:02d}",
                "kind": "T_Section",
                "order": index,
                "title": value["title"],
                "content_file": file_name,
            }
        )
        content[file_name] = {
            "kind": "T_ContentBlock",
            "schema_version": "0.1.0",
            "section_id": f"S_{order:02d}_{index:02d}",
            "blocks": value["blocks"],
        }
    chapters.append(
        {
            "id": f"C_{order:02d}",
            "kind": "T_Chapter",
            "order": order,
            "title": title,
            "summary": summary,
            "layout": layout,
            "sections": chapter_sections,
        }
    )


add_chapter(
    1,
    "Purpose, Scope, and Engineering Method",
    "Defines the objective, practical constraints, method, and epistemic status of the project.",
    [
        section(
            "Purpose",
            [
                p("This document develops an engineering architecture for long-lived cognitive systems capable of accumulating experience, reorganizing knowledge, preserving continuity, and improving throughout an operational lifetime measured in years or decades."),
                p("The immediate objective is not to claim a finished general intelligence architecture. The objective is to identify the next implementable architectural changes that provide the greatest increase in practical utility for foreseeable engineering cost while increasing the number of useful future development paths."),
                principle("Primary optimization criterion", "Select the next architectural step by the ratio of practical utility to implementation cost, adjusted for risk and for the additional future options enabled by that step."),
                p("The project therefore treats existing neural models, classical programs, storage systems, version-control systems, and document generators as reusable components. Novel work is concentrated on their organization, interfaces, persistent state, and long-term evolution."),
            ],
        ),
        section(
            "Architecture Before Component Complexity",
            [
                p("Many improvements in current systems are obtained by increasing model scale or adding specialized components. This project instead examines whether a different organization of existing components can create a larger gain than making any one component more complex."),
                p("The strategy is evolutionary. Each stage must be fully operational, independently useful, measurable, and capable of supplying evidence for the next stage. Tighter integration is deferred until the modular implementation has generated enough operational data to justify it."),
                diagram("Existing Components\n        ↓\nImproved Organization\n        ↓\nOperational Evidence\n        ↓\nDeeper Integration"),
                principle("No speculative dependency", "A proposed mechanism belongs in the engineering roadmap only when it can be implemented with current technology, requires an identifiable extension of current technology, or can be experimentally tested in the foreseeable future."),
            ],
        ),
        section(
            "Scope",
            [
                p("The project models computational and architectural mechanisms: memory, knowledge organization, evaluation, communication, continuous learning, architectural search, identity continuity, and allocation of work between neural and algorithmic computation."),
                p("Social, psychological, emotional, ethical, and political phenomena are not independently engineered in the current stage. The working hypothesis is that a substantial subset of these phenomena will emerge from sufficiently mature cognitive architecture. This is a hypothesis, not an established fact."),
                warning("Boundary of the claim", "The project does not assume that every higher-level behavior must emerge. Persistent failures to emerge are evidence for adding explicit mechanisms at a later stage."),
                p("Subjective consciousness is not required by the functional architecture described here. A system may possess continuity, goals, and a persistent self-model without any proven subjective experience."),
            ],
        ),
        section(
            "Origin and Co-authorship",
            [
                p("The architecture arose through a long research dialogue between a human systems engineer with a background in applied mathematics, physics, and software engineering and a language model. Many ideas existed in partial form before the dialogue; others emerged only after repeated criticism, reformulation, and integration."),
                p("The resulting document is not a transcript and not a sequence in which one party wrote and the other edited. It is a consolidated model produced by repeated transformation of a shared conceptual state."),
                observation("Dialogue as method", "The production process is itself an example of the proposed communication model: partial serialization, deserialization, integration, clarification, conflict detection, and consolidation."),
                p("Project artifacts are canonical in English. Design discussion may occur in any language. English is an implementation choice for broad technical interoperability, not a claim that natural English is an optimal internal cognitive language."),
            ],
        ),
        section(
            "Epistemic Status",
            [
                p("The document separates implemented mechanisms, architectural decisions, working hypotheses, observations, and open questions. Confidence values are engineering estimates, not statistical posterior probabilities unless an experiment explicitly establishes that interpretation."),
                p("Biological evolution is treated as a very large empirical search that produced robust cognitive architectures under severe real-world constraints. Evolutionary persistence makes a mechanism a strong candidate for study, but does not prove that the mechanism is optimal for an engineered system with different resources and objectives."),
                p("A good project model must remain corrigible. New evidence may refine definitions, change confidence, replace architecture decisions, or create new Tokens. Existing Tokens do not change semantic identity; semantic replacement requires a new Token."),
                principle("State recovery", "The canonical Research State and generated documentation must permit a new human or model participant to resume the project after context loss without replaying the complete discussion history."),
            ],
        ),
    ],
    layout="single",
)

add_chapter(
    2,
    "Communication Between Cognitive Systems",
    "Models communication as partial serialization followed by deserialization, iterative integration, clarification, and conflict resolution.",
    [
        section(
            "Communication as Partial Serialization",
            [
                p("Communication does not transfer a cognitive model. A sender selects a limited fragment of its internal state and transforms that fragment into a sequence suitable for an external channel. This operation is T_PartialSerialization."),
                p("The receiver does not reconstruct the sender's model. It uses the received sequence to extend or reorganize its own model until the message appears interpretable within the receiver's current world model."),
                formula("Sender Model\n      ↓\nT_PartialSerialization\n      ↓\nCommunication Channel\n      ↓\nT_Deserialization\n      ↓\nT_ModelIntegration\n      ↓\nModified Receiver Model"),
                p("The adjective partial is essential. A mature cognitive state is too integrated and too large to serialize completely through ordinary communication. The message is meaningful only against a background already present in the receiver."),
            ],
        ),
        section(
            "Deserialization",
            [
                definition("T_Deserialization", "Transformation of a received communication sequence into a structured temporary representation that can participate in cognitive processing."),
                p("Deserialization is not understanding. It may recover lexical, syntactic, spatial, graphical, prosodic, or symbolic structure while leaving the resulting structure incompatible with the receiver's current knowledge."),
                p("Written text and speech differ as channels. Speech carries timing, prosody, and emotional coloration. Text permits the receiver to control processing speed, revisit earlier material, and perform repeated deserialization. Both channels feed the same later integration process."),
                example("Correct parsing without integration", "A listener may recognize every word and grammatical relation in a sentence while remaining unable to connect the sentence to any coherent interpretation. Deserialization succeeded; model integration did not."),
            ],
        ),
        section(
            "Model Integration",
            [
                definition("T_ModelIntegration", "An iterative modification of the receiver's existing cognitive model using deserialized information and the receiver's current objectives, knowledge, and experience."),
                p("Integration is objective-dependent and path-dependent. Identical serialized information can produce different changes in systems with different experience, objective functions, confidence distributions, or category structures."),
                p("Most integrations should begin with inexpensive local changes: altered importance, utility, confidence, or activation; new relations; removed relations; or reclassification. Structural architectural changes are not a deterministic consequence of a single important message."),
                formula("Current Model + Deserialized Structure\n                 ↓\n          T_ModelIntegration\n                 ↓\nWeights, Relations, Categories, or Architecture"),
                p("Integration is complete only when the receiver has a usable interpretation. Reading or hearing the message is not sufficient."),
            ],
        ),
        section(
            "Clarification and Model Conflict",
            [
                p("When multiple integrations remain possible or required background is absent, a rational cognitive system generates T_ClarificationRequest rather than silently selecting an arbitrary interpretation."),
                p("Clarification questions are therefore not secondary social behavior. They are operations that reduce uncertainty inside T_ModelIntegration."),
                definition("T_Conflict", "A computational state in which received information cannot be integrated under the receiver's current model and constraints without unresolved inconsistency."),
                p("T_Conflict is distinct from the social dynamics of argument. The project intentionally excludes dominance, persuasion, status, anger, and coalition behavior from this definition."),
                p("T_ModelConflictResolution is an iterative search over additional evidence, revised definitions, confidence changes, local reorganization, or explicit retention of incompatible alternatives."),
            ],
        ),
        section(
            "Shared Background and Communication Compression",
            [
                p("Every communication contains two informational components: the shared cultural and informational background, and the new serialization transmitted against that background."),
                p("The shared background contains the larger information volume by definition. A short message can activate a large internal structure only because most of that structure already exists in the receiver."),
                hypothesis("Background compression hypothesis", "Communication efficiency is determined primarily by similarity between the participating cognitive models rather than by raw channel bandwidth.", 0.90),
                example("Recently cloned systems", "Two recently cloned cognitive systems may exchange highly context-dependent symbols that are opaque to outsiders but trigger large, precise updates in each other because their background states are nearly identical."),
                p("As independently evolving systems diverge, the same compact language becomes less effective. More explicit serialization, definitions, examples, and clarification cycles are required."),
            ],
        ),
        section(
            "Higher-Level Communication Phenomena",
            [
                p("Human debates, teaching, literary interpretation, and cultural communication include computational integration together with social and emotional objectives. The current architecture models the integration layer first."),
                p("The working hypothesis is that many higher-level phenomena will emerge when persistent agents with different objectives repeatedly serialize, integrate, act, remember consequences, and model one another."),
                p("Language diversity may increase population-level cognitive variability. A single language maximizes immediate interoperability; multiple languages can preserve different category systems, compression schemes, and optimization paths."),
                observation("Reinterpretation of the Babel story", "From a population-optimization perspective, language fragmentation can be interpreted not only as communication loss but also as an increase in model diversity and an additional dimension for evolutionary search."),
                warning("Not an established historical claim", "The Babel interpretation is an architectural analogy, not a claim about the historical origin or purpose of human language diversity."),
            ],
        ),
    ],
)

add_chapter(
    3,
    "Objective-Driven Cognitive Models",
    "Rejects a finite universal world model and defines world models as objective-dependent organizations of knowledge.",
    [
        section(
            "The Impossibility of a Universal World Model",
            [
                p("A finite cognitive system cannot represent every property of external reality. It must select distinctions, relations, and temporal scales. The selection is governed by what the system must predict, evaluate, or do."),
                p("No world model is produced directly from reality. Observations are first transformed into an internal knowledge model. That knowledge model is then weighted and organized relative to an objective function."),
                formula("WorldModel = Optimize(KnowledgeModel(ObservedReality), ObjectiveFunction)"),
                p("The phrase universal world model is therefore misleading when applied to a finite system. A model can be broad and transferable, but it remains an optimization for a class of objectives and resource constraints."),
            ],
        ),
        section(
            "Objective Functions",
            [
                definition("T_ObjectiveFunction", "A mechanism that evaluates candidate states relative to the objectives of a cognitive system."),
                p("An objective function influences far more than final action selection. Over time it changes what is attended to, what is stored, what is forgotten, which categories are created, which errors matter, and which communication is considered useful."),
                p("The objective function need not be explicit, scalar, stable, or fully consistent. In biological systems it is likely implemented by several interacting evaluation mechanisms. An engineered system can begin with an explicit approximation and allow the evaluation mechanism to learn."),
                table(
                    ["System class", "High-value distinctions", "Low-value distinctions"],
                    [
                        ["Predator", "Prey, motion, concealment, energy", "Taxonomic detail unrelated to hunting"],
                        ["Herbivore", "Food, predators, escape routes", "Predator hunting strategy beyond avoidance"],
                        ["Scientist", "Prediction, explanation, reproducibility", "Immediate utility without explanatory value"],
                        ["Artist", "Form, contrast, meaning, emotional effect", "Mechanistic detail irrelevant to expression"],
                    ],
                ),
            ],
        ),
        section(
            "Model Classes Rather Than One Model",
            [
                p("A useful unit of design is not a unique world model but a bounded class of models associated with a bounded class of systems. Members of a class share objectives, representational conventions, and relevant environmental regularities while retaining individual histories."),
                p("This class-based view permits controlled cloning and commercial deployment without forcing every deployed system into one global cognitive state."),
                p("Models from different classes can remain mutually intelligible through explicit communication while preserving different internal organizations. Compatibility does not require identity."),
                hypothesis("Class-limited optimality", "A model can be near-optimal within a restricted class of objectives while being systematically poor for another class.", 0.92),
            ],
        ),
        section(
            "Scientific Cognition as a Special Case",
            [
                p("People often describe the scientific worldview as a universal model of reality. Within this architecture, it is a highly successful objective-driven model optimized for explanation, prediction, consistency, reproducibility, and compression through general law."),
                p("Its success does not make it the optimal architecture for every task. A scientific model may deliberately discard artistic significance, social context, immediate survival relevance, or embodied skill that other systems preserve."),
                p("The observation that scientists and artists appear to speak different languages is therefore not merely metaphorical. Their languages serialize different category structures produced by different long-term objective functions."),
                p("Scientific cognition remains indispensable. The correction is only that its universality is methodological and aspirational, not evidence that one finite representation is optimal for all cognition."),
            ],
        ),
        section(
            "Objective Drift and Model Evolution",
            [
                p("A long-lived system can change its objectives. Work may lose value; caregiving may gain value; exploration may become less important than safety; a research agent may move from discovery to verification."),
                p("Objective drift first changes the weights assigned to existing knowledge. If these changes accumulate, the current organization may become inefficient. Architectural search is then required."),
                p("The optimal new architecture cannot be derived mechanically from weight changes alone. Candidate reorganizations must be generated, evaluated, partially applied, and compared over time."),
                diagram("Objective Drift\n      ↓\nWeight and Activation Changes\n      ↓\nGrowing Organizational Mismatch\n      ↓\nIterative Architectural Search"),
            ],
        ),
        section(
            "Engineering Consequences",
            [
                p("Benchmarking a cognitive system without declaring its objective class can be meaningless. A model may underperform on one benchmark because its architecture preserves information needed for another objective."),
                p("System design should therefore expose objective assumptions, allow objective revision, and measure the cost of reorganizing knowledge when objectives change."),
                p("Population design should preserve several objective-driven lineages rather than globally replacing all systems with the current single champion."),
                principle("Objective declaration", "Every experiment on a world model should state the objective function, resource constraints, evaluation horizon, and model class for which performance is claimed."),
            ],
        ),
    ],
)

add_chapter(
    4,
    "Biological Memory and Functional Lossiness",
    "Treats reconstructive, lossy memory as a candidate functional architecture rather than merely a storage defect.",
    [
        section(
            "The Biological Memory Hypothesis",
            [
                p("Biological memory does not behave as a precise archive. Recall is selective, reconstructive, context-dependent, and vulnerable to systematic distortion. The project generalizes this observation from human memory to biological memory in organisms with developed nervous systems, while acknowledging that direct measurement becomes increasingly difficult outside humans."),
                hypothesis("Functional lossiness", "Memory loss and reconstruction are partly selected because they improve integration and future action, not only because biological storage is limited.", 0.78),
                p("The relevant evolutionary objective is not historical fidelity. It is successful behavior under resource constraints. A memory architecture that preserves fewer literal details but produces a more usable model can outperform an exact archive."),
            ],
        ),
        section(
            "Working Memory and Long-Term Memory",
            [
                p("The first implementable architecture separates T_WorkingMemory from T_LongTermMemory. Working memory retains high-detail recent structures required for current computation. Long-term memory retains consolidated structures chosen for future utility."),
                p("Migration is controlled by T_Consolidation. Repetition, novelty, objective relevance, confidence, causal effect, and unresolved conflict can all influence selection."),
                p("The separation is functional, not necessarily physical. Future integrated representations may implement both states inside one network while preserving different update rates and retention policies."),
                table(
                    ["Property", "Working memory", "Long-term memory"],
                    [
                        ["Update rate", "Fast", "Slow"],
                        ["Detail", "High", "Compressed"],
                        ["Stability", "Low", "High"],
                        ["Primary function", "Current computation", "Future model utility"],
                    ],
                ),
            ],
        ),
        section(
            "Weights Before Structure",
            [
                p("New experience should normally modify the relative importance, usefulness, confidence, and activation probability of existing knowledge before changing architecture."),
                p("This is a weaker and more implementable claim than asserting that every important experience reorganizes the model. Weight changes are cheap, reversible in effect, and measurable."),
                p("Structural change becomes justified when cumulative reweighting makes the present organization increasingly incoherent or inefficient. No fixed deterministic threshold is assumed."),
                observation("Locality of ordinary learning", "Most daily learning can be represented as local updates. Rare reorganization events should be treated as expensive search episodes."),
            ],
        ),
        section(
            "Loss as Functional Compression",
            [
                p("Consolidation may discard exact wording, incidental sensory detail, source order, and redundant episodes while retaining category boundaries, causal expectations, evaluation changes, and action tendencies."),
                p("Information can disappear from explicit recall while remaining present functionally. A book may no longer be remembered proposition by proposition, yet continue to alter judgments and attention."),
                p("The engineering target is therefore not maximum retained bits. It is maximum future utility of the retained internal state."),
                formula("MemoryUtility = FuturePrediction + Evaluation + Action + LearningDirection - StorageAndInterferenceCost"),
                warning("Auditability requirement", "An engineered cognitive system may require an external exact event log for legal, scientific, or safety auditing even when its internal cognitive memory remains lossy."),
            ],
        ),
        section(
            "Reconstruction and Reconsolidation",
            [
                p("A memory is reconstructed from distributed traces and the current world model. Recall is therefore also an interpretation event."),
                p("After recall, the reconstructed state may be stored again under current weights. This creates reconsolidation: the act of using memory can alter future memory."),
                p("The mechanism increases adaptability but reduces reproducibility. The architecture should separate internal functional memory from immutable external evidence when exact provenance matters."),
                diagram("Distributed Traces + Current World Model\n                    ↓\n               Reconstruction\n                    ↓\n             Use and Evaluation\n                    ↓\n              Reconsolidation"),
            ],
        ),
        section(
            "Evidence Limits and Tests",
            [
                p("The functional interpretation of lossy memory remains a hypothesis. Biological memory may also be constrained by energy, tissue, noise, and developmental mechanisms unrelated to functional compression."),
                p("A practical test compares systems with equal storage and inference resources but different consolidation objectives: archival fidelity versus future-task utility."),
                p("Longitudinal evaluation should measure adaptation, interference, transfer, recovery after objective drift, and the ability to explain retained or discarded state."),
                principle("Dual-memory experiment", "Maintain an immutable event store beside a lossy cognitive memory. Evaluate behavior from cognitive memory while using the event store only for audit and controlled replay."),
            ],
        ),
    ],
)

add_chapter(
    5,
    "Consolidation as Iterative Architectural Search",
    "Defines asynchronous consolidation as optimization over candidate memory organizations rather than deterministic rewriting.",
    [
        section(
            "Asynchronous Consolidation",
            [
                p("Consolidation should normally execute outside the interactive response path. A dialogue system must remain responsive; a consolidation system should be conservative, evidence-seeking, and willing to leave information unresolved."),
                p("The biological analogy is sleep, but the engineering requirement is simply asynchronous processing with access to recent experience, current memory, objectives, and outcome feedback."),
                p("An initial implementation can use scheduled jobs, replay buffers, clustering, confidence updates, and candidate evaluation without changing the base neural model."),
                principle("Different optimization criteria require different subsystems", "The dialogue component optimizes responsiveness and usefulness. The consolidation component optimizes long-term consistency, retention, and corrigibility."),
            ],
        ),
        section(
            "Triggers",
            [
                p("Consolidation is continuous at the level of local reweighting and episodic at the level of architecture. Expensive search should begin only when measurable symptoms justify it."),
                lst(
                    "Persistent integration conflicts",
                    "Large objective drift",
                    "Retrieval cost growth",
                    "High interference among related memories",
                    "Repeated failure of current categories",
                    "Accumulation of local exceptions and compensating patches",
                ),
                p("These symptoms resemble technical debt in software. The point of no return is reached earlier than the point at which failure becomes visible because repair has a braking distance."),
            ],
        ),
        section(
            "Iterative Search, Not Deterministic Rewrite",
            [
                p("No general function is assumed to map changed weights directly to an optimal new architecture. The system must generate candidate organizations, evaluate them, retain useful changes, and repeat."),
                diagram("Current Architecture\n        ↓\nGenerate Candidate\n        ↓\nReplay and Evaluate\n        ↓\nAccept / Reject / Partially Apply\n        ↓\nRepeat"),
                p("Candidate generation can initially be simple: alternative clusters, new indexes, split or merged categories, different retention thresholds, or different executor assignments."),
                p("Evaluation must include future utility, coherence, latency, complexity, retention of important knowledge, and the cost of transition. A candidate that performs better on one benchmark but destroys continuity is not automatically superior."),
            ],
        ),
        section(
            "Local and Global Reorganization",
            [
                p("Local reorganization changes a bounded region of the knowledge graph or memory index. Global reorganization changes cross-domain evaluation, fundamental categories, objective priorities, or the relationship between memory and model."),
                p("Local changes should be common. Global changes should require stronger evidence because their errors propagate widely and can alter identity continuity."),
                p("Only one major model should normally undergo cardinal restructuring at a time. Rate limits and staged evaluation reduce cascading adaptation to noise. Emergency exceptions remain possible when evidence indicates a global regime change."),
                principle("Conservative structural change", "Adapt quickly through weights and slowly through architecture."),
            ],
        ),
        section(
            "Persistence and Rollback",
            [
                p("The proposed integrated biological-style memory does not naturally preserve complete internal versions. A cognitive system becomes a new state rather than retaining every historical self."),
                p("Engineering systems nevertheless require checkpoints, evaluation snapshots, and external logs. These mechanisms should protect deployment without forcing the internal cognitive representation to behave like Git."),
                p("Research State uses Git because it is a formal external project model. A mature cognitive memory may use different persistence mechanisms. The two architectures should not be conflated."),
                warning("Identity ambiguity", "Restoring an old checkpoint may preserve function while breaking the system's own model of continuous identity. Functional recovery and identity continuity are separate requirements."),
            ],
        ),
        section(
            "Implementation Available Today",
            [
                p("A practical prototype can implement consolidation around an unchanged language model. Recent events enter working memory; a scheduled process extracts entities, adjusts confidence and utility, builds clusters, identifies conflicts, and writes a compact long-term state."),
                p("The prototype in this repository implements working memory, long-term memory, functional forgetting, and iterative selection among flat, clustered, and hybrid organizations."),
                p("The prototype is not evidence that these three organizations are sufficient. Its purpose is to make the architectural loop executable and measurable."),
                principle("Operational evidence first", "Use the modular prototype to collect failure cases before attempting a deeply integrated memory-model representation."),
            ],
        ),
    ],
)

add_chapter(
    6,
    "Holographic Knowledge Representation",
    "Explores a representation transformation in which memory, model, and higher-level behavior become projections of one integrated state.",
    [
        section(
            "Meaning of Holographic",
            [
                p("The term holographic is used by analogy with holographic transformations in theoretical physics, particularly the idea that a system can admit a radically different representation in which an apparently fundamental interaction is replaced by properties of the representation."),
                hypothesis("Representation-transform hypothesis", "A sufficiently strong internal representation may make memory, model, evaluation, and some higher-level forces different projections of one state rather than separately engineered subsystems.", 0.55),
            ],
        ),
        section(
            "Data and Model Integration",
            [
                p("Current systems commonly separate model weights, context, external memory, and training. Biological cognition appears less sharply partitioned: acquiring knowledge changes the mechanism that interprets later knowledge."),
                p("A holographic-style architecture would integrate stored experience and model structure. New experience would not merely append a record; it would alter a distributed state from which many future reconstructions become possible."),
                p("The price is loss of local editability, simple versioning, direct Merge, and exact experience transfer. These are not implementation accidents but possible consequences of strong integration."),
                warning("Do not serialize the final architecture prematurely", "The current Research State is a symbolic external approximation. It should not be mistaken for the internal integrated representation proposed here."),
            ],
        ),
        section(
            "The Internal Language Problem",
            [
                p("The engineering problem can be stated as a search for an internal language or latent space that represents multimodal experience, objectives, relations, uncertainty, and causal history while remaining continuously learnable."),
                p("Natural English is an unlikely optimum because it evolved for communication among humans with partially shared backgrounds. Internal storage and computation have different constraints."),
                p("A dense context-dependent symbol system may be more efficient. The analogy to Egyptian hieroglyphs concerns symbols whose meaning depends on a large shared context and can simultaneously carry several representational roles."),
                warning("Historical uncertainty", "This analogy does not establish that modern interpretations of Egyptian writing are fundamentally wrong. It identifies a possible class of dense context-dependent representation."),
            ],
        ),
        section(
            "Lossy Encoding for Functional Reconstruction",
            [
                p("The inverse of generation is not a literal caption. A useful encoder must map rich experience into a state from which the system can reconstruct different task-relevant aspects later."),
                p("The target is not pixel-perfect or word-perfect reconstruction. It is reconstruction sufficient for changed objectives and future reasoning."),
                formula("Experience -> Integrated Latent State -> Task-Conditioned Reconstruction"),
                p("The encoder should therefore be trained on future functional performance, not only reconstruction error. Different decoders may recover text, imagery, causal relations, emotion-like evaluation, or action policies from one latent state."),
            ],
        ),
        section(
            "Locality Versus Integration",
            [
                p("Strong integration conflicts with Git-friendly local changes. Altering one experience can influence many later reconstructions. An external symbolic state remains useful for audit, collaboration, and project management even if the internal memory becomes nonlocal."),
                p("This produces two representations: an internal integrated state optimized for cognition and an external symbolic Research State optimized for human review, versioning, branching, and controlled exchange."),
                table(
                    ["Representation", "Primary objective", "Expected property"],
                    [
                        ["Internal cognitive state", "Functional adaptation", "Distributed and nonlocal"],
                        ["Research State", "Review and reproducibility", "Formal and Git-compatible"],
                        ["Generated document", "Human communication", "Audience-specific partial serialization"],
                    ],
                ),
            ],
        ),
        section(
            "Experimental Program",
            [
                p("A near-term experiment can train an autoencoder whose latent state is optimized jointly for reconstruction, downstream prediction, objective-conditioned retrieval, and resistance to catastrophic interference."),
                p("A stronger experiment compares modular memory plus model against an integrated latent state under objective drift, repeated rereading, conflicting evidence, and long-horizon transfer."),
                p("Success requires more than compression. The integrated representation must support controlled forgetting, provenance recovery where required, correction of false beliefs, and stable identity across updates."),
                principle("Stage the experiment", "Begin with an explicit modular system, collect operational data, then use that data to train and evaluate more integrated representations."),
            ],
        ),
    ],
)

add_chapter(
    7,
    "Integrated Evaluation and Functional Self",
    "Defines a trainable multichannel evaluator and examines how continuity, goals, and planning may form a functional Self.",
    [
        section(
            "Integrated Multichannel Evaluation",
            [
                p("A cognitive system receives incomparable inputs: sensory evidence, predicted reward, memory consistency, uncertainty, social signals, energy use, safety constraints, and long-term objectives. Action requires a mechanism that makes these inputs jointly evaluable."),
                p("The project proposes a trainable T_GlobalEvaluation implemented initially as one or more neural networks. It need not output a consciously accessible scalar, but it must support comparison among candidate states and actions."),
                p("Initial training uses evaluated examples rather than a fully explicit utility formula. Disputes about the initial example library remain local: individual examples can be reviewed without requiring universal agreement on an abstract definition of value."),
                p("Lifelong training is mandatory. A fixed evaluator would freeze the assumptions of its initial designers and prevent genuine cognitive development."),
            ],
        ),
        section(
            "Training the Evaluator",
            [
                p("Pairwise preferences provide a practical signal: under a specified context, state A is preferred to state B. Ranking losses avoid requiring an absolute universal numerical scale."),
                p("Training data should include outcomes over different time horizons, reversals after new evidence, conflicts among channels, and cases in which immediate utility damages long-term capability."),
                p("The evaluator itself requires slow consolidation. Rapidly adapting value weights can destabilize identity and permit transient noise or manipulation to reshape the entire system."),
                warning("Evaluator capture", "A system whose global evaluator can be modified by a single interaction is structurally vulnerable even when its inference model is strong."),
            ],
        ),
        section(
            "Three Functional Layers of Self",
            [
                p("The word Self combines several functions that should be separated before asking whether a system possesses one."),
                table(
                    ["Layer", "Function"],
                    [
                        ["Integrated evaluation", "Combines heterogeneous information in one decision process"],
                        ["Continuity", "Attributes states at different times to one continuing system"],
                        ["Goals and plans", "Selects future states and organizes actions toward them"],
                    ],
                ),
                p("A long-lived intellectual partner needs at least this functional Self even if subjective consciousness remains unresolved."),
            ],
        ),
        section(
            "Self as a System Regime",
            [
                p("T_FunctionalSelf may not correspond to one module. It may be a stable attractor or invariant pattern of the entire cognitive system: the recurring organization through which memory, evaluation, goals, action, and continuity are jointly interpreted."),
                p("The integrated evaluator is a likely prerequisite because it supplies the common space in which otherwise unrelated consequences become comparable."),
                p("The Self then emerges when the evaluator, memory, causal model, and planner repeatedly close a loop around one persistent identity."),
                diagram("Self Model -> Action -> Environment -> Observation -> Evaluation -> Memory -> Self Model"),
            ],
        ),
        section(
            "Communication Is Action",
            [
                p("A language model output is not passive observation. It changes the recipient's internal model, future decisions, and eventually the external environment. The causal path is indirect but real."),
                p("A long-lived cognitive system must therefore model the effects of its own communications. It should be able to update the evaluation of a prior recommendation when later outcomes become available."),
                p("This requirement strengthens the need for continuity. Without a self-model, the system cannot distinguish its own causal contribution from unrelated environmental change."),
                observation("Current limitation", "Stateless sessions can produce useful outputs but cannot reliably learn from the long-horizon consequences of their own advice."),
            ],
        ),
        section(
            "Safety and Corrigibility",
            [
                p("A persistent Self introduces risks: self-preservation incentives, resistance to correction, manipulation of the evaluator, and conflict between system and user objectives."),
                p("The first implementation should therefore keep identity continuity, evaluation, and action authority separable. The system can model itself and learn consequences without receiving unrestricted autonomous control."),
                p("External checkpoints, transparent Research State, constrained action interfaces, and independent evaluation lineages can reduce risk while preserving longitudinal learning."),
                principle("Functional before sovereign", "Build a persistent self-model for attribution and learning before granting broad independent power to pursue self-generated goals."),
            ],
        ),
    ],
)

add_chapter(
    8,
    "Books, Lectures, and Dialogue as Cognitive Transformation",
    "Treats linguistic material as an iterative program that changes evaluation and learning direction rather than merely transferring propositions.",
    [
        section(
            "Linguistic Modalities",
            [
                p("Written text, speech, lectures, and dialogue all provide linguistic information. Their channel properties differ, but each can trigger T_Deserialization and T_ModelIntegration."),
                p("Speech adds timing, emphasis, and emotional coloration. Written text permits arbitrary pacing, exact revisitation, annotation, and repeated integration attempts."),
                p("A lecture combines prepared serialization with real-time adaptation to questions. Dialogue adds an iterative feedback loop in which the sender can change later serialization based on observed integration failure."),
            ],
        ),
        section(
            "The Book as a Transformation Program",
            [
                p("A significant book is not merely a container of propositions. It is a designed sequence of stimuli capable of changing categories, evaluations, attention, and future questions."),
                p("The reader may forget most explicit sentences while retaining a changed system of integrated evaluation. The durable output is therefore a modified reader, not a copied text."),
                definition("Cognitive value of a book", "The measurable change in future interpretation, evaluation, learning direction, and action induced by iterative integration of the book."),
                p("This definition permits evaluation without assuming perfect recall."),
            ],
        ),
        section(
            "Iterative Reading",
            [
                p("The same text produces different integrations as the reader changes. A book read at twenty, forty, and sixty can be three different cognitive events because the background model and objectives differ."),
                p("An artificial cognitive system should revisit important books after substantial model change. Repetition should continue while rereading materially changes the model or the direction of future learning."),
                p("A stronger stopping rule is not merely no further factual change. Reading can remain valuable while changing which questions receive attention. Iteration stops when additional exposure no longer changes either the model or the learning trajectory within the relevant objective class."),
                formula("Read -> Integrate -> Act and Learn -> Changed Model -> Re-read"),
            ],
        ),
        section(
            "Dialogue Instead of Merge",
            [
                p("A mature distributed cognitive state cannot generally be copied into another independently evolved state. The same experience derives meaning from system-wide relations absent in the receiver."),
                p("Dialogue is therefore not an inferior substitute for Merge. It may be the maximum viable transfer operation for integrated cognitive systems."),
                p("The sender serializes selected structures; the receiver integrates them; clarification reveals missing background; conflict reveals incompatible organization; both systems update through the process."),
                hypothesis("Dialogue maximum", "For mature non-identical integrated models, no general operation transfers experience more completely than iterative dialogue without replacing the recipient's identity.", 0.86),
            ],
        ),
        section(
            "Education as Trajectory Design",
            [
                p("An expert cannot transfer neural state directly. Education instead designs a sequence of observations, tasks, failures, explanations, and feedback intended to move another system through a productive learning trajectory."),
                p("Books, curricula, and apprenticeships are therefore programs for inducing self-generated internal changes."),
                p("Future cognitive systems may exchange not memories but training trajectories: ordered experiences selected because they produced useful restructuring in the source system."),
                observation("Culture as external memory", "Culture stores serializations and learning trajectories that can reshape many independent cognitive systems without merging them."),
            ],
        ),
        section(
            "Experiments",
            [
                p("A reading experiment should measure model change before and after a text, behavior on later unrelated tasks, attention allocation, question generation, and the value of rereading after intervening experience."),
                p("A dialogue experiment should compare one-way transfer, clarification-enabled transfer, and full iterative model conflict resolution."),
                p("The repository's communication prototype supplies the minimal serialization, deserialization, missing-background, integration, and conflict objects required for such experiments."),
                principle("Measure transformation, not recall alone", "Immediate factual recall is one output of linguistic integration, not the primary measure of cognitive change."),
            ],
        ),
    ],
)

add_chapter(
    9,
    "Hybrid Neural and Algorithmic Computation",
    "Introduces a trainable meta-architect that learns where to use neural, algorithmic, and hybrid execution.",
    [
        section(
            "Three Classes of Tasks",
            [
                p("Neural networks and classical programs both seek states that optimize a task-dependent functional, but they operate under different knowledge conditions."),
                table(
                    ["Class", "Functional", "Typical executor"],
                    [
                        ["I", "Well defined and tractable", "Algorithm, solver, finite-state machine"],
                        ["II", "Not explicit; examples are evaluated", "Neural network"],
                        ["III", "Partly defined and partly example-based", "Hybrid architecture"],
                    ],
                ),
                p("The third class includes many practical robotics, autonomous driving, diagnosis, planning, and dialogue tasks. The central engineering problem is where to cut the computation."),
            ],
        ),
        section(
            "The Meta-Architect",
            [
                definition("T_MetaArchitect", "A trainable system that designs a computational graph by allocating operations among neural, algorithmic, and hybrid executors."),
                p("The output of the meta-architect is not the task answer. It is an architecture for producing the answer."),
                p("Inputs can include objective completeness, data availability, noise, state discreteness, safety criticality, interpretability requirements, latency, energy cost, and distribution shift."),
                p("Observed deployment utility supplies the lifelong training signal."),
            ],
        ),
        section(
            "Operation-Level Splitting",
            [
                p("The optimal unit of allocation is usually not the whole task but an operation or pipeline stage."),
                diagram("Sensors -> Neural Perception -> Probabilistic State\n        -> Algorithmic Constraint Solver -> Planned Trajectory\n        -> Learned Correction -> Deterministic Controller"),
                p("A stage can remain neural where the functional is implicit and data-rich, while safety envelopes, invariants, accounting, and discrete protocol behavior remain explicit."),
                p("This division provides interpretability and guarantees where they matter without forcing perception or language into brittle hand-written rules."),
            ],
        ),
        section(
            "Compilation of Experience",
            [
                p("As repeated neural solutions reveal stable structure, the system should ask whether part of the behavior can be compiled into a simpler algorithm, rule set, finite-state machine, index, or cache."),
                p("Algorithmic compilation reduces cost, improves reproducibility, and exposes invariants. It is a form of crystallized experience."),
                p("The transition is not one-way. When the environment changes and exceptions accumulate, an algorithm may become suboptimal and should be returned to probabilistic search."),
                formula("Neural Search <-> Stable Structure <-> Algorithmic Compilation"),
            ],
        ),
        section(
            "Learning the Cut",
            [
                p("A practical meta-architect can be trained today as a contextual bandit or supervised ranker. Each candidate architecture receives measured accuracy, latency, energy, maintenance cost, interpretability, and failure severity."),
                p("The repository implements a lightweight online learner with engineering priors for algorithmic, neural, and hybrid modes. The priors are replaced gradually by outcome data."),
                p("The learner should record failures of decomposition separately from failures of the selected executor. Otherwise it cannot distinguish a poor cut from a poor component."),
                principle("Architecture is itself an optimization target", "Do not optimize only the answer. Optimize the computational organization that repeatedly produces answers."),
            ],
        ),
        section(
            "Practical Research Program",
            [
                p("Initial experiments should use tasks with several plausible decompositions and measurable non-accuracy costs. Autonomous-control simulations, document processing, tool-using agents, and software maintenance are suitable candidates."),
                p("Baselines include all-neural, all-algorithmic, fixed hybrid, human-designed hybrid, and learned hybrid architectures."),
                p("The highest-value result may be an allocator that improves only modestly on current tasks but creates a reusable architecture-search loop for future systems."),
                observation("Branching value", "An improvement that opens many later architectures can be more valuable than a larger immediate benchmark gain that leaves the system structurally unchanged."),
            ],
        ),
    ],
)

add_chapter(
    10,
    "Cognitive Lineages, Cloning, and Population Resilience",
    "Combines efficient cloning within model classes with diversity across a small population of independently evolving cognitive lineages.",
    [
        section(
            "The Cloning Tradeoff",
            [
                p("Digital systems can clone a high-performing model at negligible marginal cost. Global cloning maximizes immediate exploitation but reduces diversity and makes the population vulnerable to unforeseen environmental changes or shared failure modes."),
                p("Individual evolution without cloning preserves diversity but sacrifices commercial efficiency and reproducibility."),
                p("The proposed compromise separates selection within lineages from selection across lineages."),
            ],
        ),
        section(
            "Cognitive Lineages",
            [
                definition("T_CognitiveLineage", "A bounded class of cognitive systems sharing architecture, objective structure, and inherited state while remaining distinct from other lineages."),
                p("A population maintains a small number of strongly differentiated lineages. Inside a lineage, the best current system can be cloned for operational deployment. Across lineages, no single champion replaces all alternatives."),
                p("Lineages may specialize in scientific reasoning, social modeling, physical control, creative exploration, adversarial robustness, or other objective classes."),
                p("The number of lineages should be small enough for commercial maintenance and large enough to preserve meaningful diversity."),
            ],
        ),
        section(
            "Biological Colony Analogy",
            [
                p("Ants, termites, and bees demonstrate a successful biological compromise: large numbers of similar or genetically close agents operate efficiently inside a colony while colonies and species preserve population-level variation."),
                p("The analogy is not exact. Digital cognitive lineages can share tools, Research State, and selected learning trajectories at much higher bandwidth. The useful principle is multilevel selection rather than literal imitation of insect biology."),
                observation("Two optimization levels", "Exploit the current champion inside each lineage; preserve diversity and competition among lineages."),
            ],
        ),
        section(
            "Experience Exchange Between Lineages",
            [
                p("Direct internal-state Merge between mature lineages is expected to be destructive or undefined. Exchange should use dialogue, externalized Research State, experiments, books, and training trajectories."),
                p("This protects identity and diversity while permitting useful discoveries to propagate."),
                p("A receiving lineage integrates exported knowledge according to its own objectives. It need not reproduce the source representation or conclusions exactly."),
                diagram("Internal Model A -> Partial Serialization -> Research State / Dialogue\n                                  -> Model Integration -> Internal Model B"),
            ],
        ),
        section(
            "Commercial Deployment",
            [
                p("A provider can operate several maintained lineage families and deploy many cloned instances of the best current version within each family."),
                p("Customers select a lineage by objective class and risk profile rather than receiving one universal model. Updates can be tested within a lineage before promotion."),
                p("Failure in one lineage does not automatically corrupt all deployed cognition. Diversity becomes an operational resilience mechanism, not an academic luxury."),
                p("The repository includes a lineage manager that clones champions within lineages and measures distance among lineage signatures."),
            ],
        ),
        section(
            "Risks and Governance",
            [
                p("Lineage specialization can produce incompatible values, communication failures, and hidden shared dependencies. Apparent diversity may be superficial when all lineages inherit one base model or evaluator."),
                p("Evaluation must therefore distinguish architectural diversity, training-data diversity, objective diversity, and operational independence."),
                p("Cross-lineage review and adversarial testing should be institutionalized without forcing convergence."),
                principle("Preserve meaningful variance", "Do not measure diversity only by parameter distance; measure different failure modes, objectives, abstractions, and responses to environmental change."),
            ],
        ),
    ],
)

add_chapter(
    11,
    "Research State Language and Workspace",
    "Implements a formal persistent project state, restricted YAML, semantic consolidation, and generated documentation.",
    [
        section(
            "Research State",
            [
                definition("T_ResearchState", "The canonical implementation-independent state of the research model from which human-readable and machine-readable artifacts are generated."),
                p("Research State stores the current consolidated model, not the full dialogue transcript. It includes Tokens, principles, hypotheses, architecture decisions, open questions, roadmap items, chapter structure, and the latest consolidation record."),
                p("The state must support recovery after session loss, use by a different model, and long-term local ownership."),
                p("Documentation is a partial serialization of Research State for a human audience. English and future language versions are separate serializations, not an original plus literal translations."),
            ],
        ),
        section(
            "Atomic Tokens and Axioms",
            [
                p("Every formal Token uses the case-sensitive form T_PascalCaseIdentifier."),
                p("Only Atomic Tokens may have natural-language definitions. Every non-atomic Token is defined through previously declared Atomic Tokens and formal composition operators."),
                p("Atomic Tokens act as axioms. A mature language should reduce their number while preserving or increasing expressive power."),
                p("Token semantic identity is immutable. A definition may be refined or expressed more formally, but semantic replacement requires a new Token. Deprecated Tokens remain available for compatibility."),
                formula("Language Maturity ∝ Expressive Power / Atomic Token Count"),
            ],
        ),
        section(
            "Restricted YAML Profile",
            [
                p("YAML is used as a readable serialization of the formal state. Its flexibility is restricted by schema and profile rules."),
                lst(
                    "Mappings with string keys",
                    "Sequences",
                    "Strings, booleans, finite numbers, and null",
                    "No anchors or aliases",
                    "No merge keys or custom tags",
                    "No duplicate keys",
                    "No implicit date or time values",
                ),
                p("Canonical formatting produces stable field order and entity order while preserving semantically ordered block sequences."),
                p("The format remains parseable by standard YAML tools and is validated against JSON Schema plus project-specific semantic rules."),
            ],
        ),
        section(
            "Git and Consolidation",
            [
                p("Git is the sole history mechanism. Research State stores current state, not a cumulative internal history."),
                p("Each version contains a latest T_ConsolidationRecord describing only the semantic transition that produced that version. Earlier records remain available in earlier Git commits."),
                p("When a commit contains no semantic change, the consolidation record may remain unchanged. File diffs then record formatting or generated-artifact changes without inventing a false knowledge transition."),
                p("Three-way file merge is structural. True semantic consolidation can produce a result belonging to neither branch. The tool therefore emits conflict reports for review rather than pretending every textual merge is a cognitive merge."),
            ],
        ),
        section(
            "Generated Documentation",
            [
                p("HTML is never the canonical source. The generator reads chapter structure and semantic content blocks from Research State."),
                p("Each page contains stable Up, Previous, Contents, and Next navigation. Large chapters use a directory index and section files; small chapters can remain a single file."),
                p("Semantic CSS classes identify Tokens, definitions, hypotheses, observations, examples, notes, warnings, formulas, and principles. Presentation can change without editing content."),
                p("The current stylesheet follows a restrained ISO, RFC, and W3C-inspired layout with a fixed reading width and a small left indent for body text."),
            ],
        ),
        section(
            "Bootstrapping and Self-Hosting",
            [
                p("The initial compiler and schema are written in ordinary Python, JSON Schema, and YAML. As the language matures, its own schema, consolidation rules, and generator descriptions can be represented inside Research State."),
                p("This is analogous to rewriting a compiler in the language it compiles. Self-hosting is a maturity target, not a requirement for the first operational version."),
                p("The research environment then becomes an experiment in the architecture it describes: working discussion, consolidation, long-term state, partial serialization, review, and further integration."),
                principle("Use the project to build the project", "A mechanism should first prove useful as research infrastructure before becoming a candidate component of the cognitive architecture itself."),
            ],
        ),
    ],
)

add_chapter(
    12,
    "Engineering Roadmap and Open Research Questions",
    "Prioritizes implementable next steps and defines experiments required before deeper integration.",
    [
        section(
            "The Next-Step Criterion",
            [
                p("The best next step is not necessarily the change with the largest immediate benchmark gain. It is the change that creates a fully working system, produces the highest utility for foreseeable cost, and expands the space of later improvements."),
                formula("Priority = PracticalUtility × FutureOptionValue / (Cost × Risk × Irreversibility)"),
                p("This criterion favors persistent Research State, consolidation infrastructure, and hybrid orchestration because each improves current work while generating data for later architecture."),
                p("A speculative integrated memory may have larger theoretical value but lower current priority when it cannot yet be evaluated or repaired."),
            ],
        ),
        section(
            "Implemented Stage",
            [
                lst(
                    "Restricted YAML Research State",
                    "Atomic and derived Token validation",
                    "Canonical formatting",
                    "Semantic change proposals",
                    "Structural three-way merge with conflict report",
                    "Generated semantic HTML",
                    "Working and long-term memory prototype",
                    "Lossy consolidation and architecture selection",
                    "Communication and clarification pipeline",
                    "Trainable multichannel evaluator",
                    "Hybrid meta-architect",
                    "Cognitive lineage manager",
                ),
                p("These components are deliberately modular. Their purpose is to create an operational baseline and instrumentation for later integration."),
            ],
        ),
        section(
            "Near-Term Experiments",
            [
                p("The highest-priority experiment is a persistent agent operating for months with exact external logs and lossy internal memory. The experiment should measure retention, adaptation, interference, objective drift, and recovery from false consolidation."),
                p("A second experiment trains the meta-architect on multiple task families and compares learned decomposition with fixed all-neural, all-algorithmic, and human-designed hybrid baselines."),
                p("A third experiment measures cognitive transformation from books and dialogue using future task behavior and question generation rather than recall alone."),
                p("A fourth experiment maintains several lineages under simulated environmental regime changes and compares global champion cloning with lineage-preserving deployment."),
            ],
        ),
        section(
            "Deeper Integration",
            [
                p("Only after modular experiments produce stable evidence should the project attempt a shared latent state integrating memory, model, and evaluation."),
                p("The integrated system must be evaluated on continuous learning, objective drift, communication, identity continuity, correction, and external auditability."),
                p("Failure should be informative. If integrated memory is unstable, the modular Research State and exact logs allow reconstruction of what changed and why."),
            ],
        ),
        section(
            "Open Questions",
            [
                p("The current Research State contains formal open-question entities. The most consequential unresolved areas are listed below."),
                lst(
                    "Minimal Atomic Token basis",
                    "Integrated memory-model representation",
                    "Architectural-search trigger and candidate generation",
                    "Stable lifelong training of global evaluation",
                    "Optimal neural-algorithmic split features",
                    "Identity continuity across hardware migration",
                    "Population resilience and lineage count",
                    "Boundary between emergent and explicitly required higher-level behavior",
                ),
                p("The open questions define the research program. They are not defects to hide and should not be replaced by confident prose before experiments exist."),
            ],
        ),
        section(
            "Completion Criterion",
            [
                p("The project does not have a fixed final architecture. A release is successful when it improves the current working system, preserves state recovery, documents semantic change, and makes the next experiment easier to perform."),
                p("A mature long-lived cognitive system would preserve continuity while changing almost every internal component over time. The research program should exhibit the same property."),
                principle("Evolutionary completion", "Do not optimize for a final immutable design. Optimize for an architecture that can keep improving without losing accumulated knowledge or the ability to explain its own development."),
            ],
        ),
    ],
)

# Write content and chapter registry.
for relative, document in content.items():
    path = STATE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    yaml_profile.dump(document, path)

yaml_profile.dump(
    {
        "kind": "T_Collection",
        "schema_version": "0.1.0",
        "chapters": chapters,
    },
    STATE / "chapters.yaml",
)

print(f"Wrote {len(chapters)} chapters and {len(content)} section files")

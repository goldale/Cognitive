from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cogsys import yaml_profile  # noqa: E402

STATE = ROOT / "state"
CONTENT = STATE / "content"
CONTENT.mkdir(parents=True, exist_ok=True)


def write(name: str, value: object) -> None:
    yaml_profile.dump(value, STATE / name)


def atomic(token: str, definition: str, status: str = "T_Active") -> dict:
    return {
        "token": token,
        "atomic": True,
        "definition": definition,
        "status": status,
    }


def derived(token: str, *arguments: str, operator: str = "T_Composition", status: str = "T_Active") -> dict:
    return {
        "token": token,
        "atomic": False,
        "expression": {
            "operator": operator,
            "arguments": list(arguments),
        },
        "status": status,
    }


atomic_tokens = [
    atomic("T_Token", "A case-sensitive symbol with stable semantic identity."),
    atomic("T_Entity", "A separately addressable object in a formal state."),
    atomic("T_System", "A bounded set of interacting elements."),
    atomic("T_State", "A configuration of a system at a specified time."),
    atomic("T_Information", "A constraint that reduces uncertainty among possible states."),
    atomic("T_Knowledge", "Information integrated into a model and usable for evaluation or action."),
    atomic("T_Model", "An internal structure used to predict, explain, evaluate, or act."),
    atomic("T_Objective", "A condition toward which optimization is directed."),
    atomic("T_Function", "A mapping from inputs to outputs."),
    atomic("T_Process", "A sequence of state transformations."),
    atomic("T_Transformation", "A change from one state or representation to another."),
    atomic("T_Relation", "A formally represented dependency between entities."),
    atomic("T_Time", "An ordering dimension for state transitions."),
    atomic("T_Memory", "A mechanism by which prior state influences future computation."),
    atomic("T_Observation", "Information acquired from an environment or another system."),
    atomic("T_Evaluation", "Assignment of relative preference, relevance, or utility."),
    atomic("T_Optimization", "Search for a state with improved evaluation."),
    atomic("T_Structure", "An organization of entities and relations."),
    atomic("T_Channel", "A medium through which a serialized state is transmitted."),
    atomic("T_Serialization", "Transformation of internal structure into a transmissible sequence."),
    atomic("T_Communication", "Interaction through transmitted information."),
    atomic("T_Conflict", "An incompatibility that prevents simultaneous integration under current constraints."),
    atomic("T_Collection", "A bounded group of entities."),
    atomic("T_Constraint", "A rule restricting valid states or transformations."),
    atomic("T_Algorithm", "An explicit finite procedure for a class of computations."),
    atomic("T_NeuralNetwork", "A trainable distributed function approximator."),
    atomic("T_Cognition", "Acquisition, integration, evaluation, and use of knowledge."),
    atomic("T_Identity", "A persistent criterion by which states are attributed to one continuing system."),
    atomic("T_Agent", "A system capable of selecting actions."),
    atomic("T_Environment", "The external state with which a system interacts."),
    atomic("T_Experience", "An observation together with its effects on a system."),
    atomic("T_Evidence", "Information used to update confidence in a claim."),
    atomic("T_Uncertainty", "A distribution over unresolved alternatives."),
    atomic("T_Language", "A formal or natural system of serializable symbols and composition rules."),
    atomic("T_Document", "A persistent serialized artifact intended for interpretation."),
    atomic("T_History", "An ordered record of prior states or transformations."),
    atomic("T_Architecture", "The organization and interaction rules of system components."),
    atomic("T_Question", "A specification of information or resolution that is missing."),
    atomic("T_Action", "A state transformation initiated by an agent."),
    atomic("T_Lineage", "A class of systems connected by controlled replication and evolution."),
    atomic("T_Active", "A status indicating current use."),
    atomic("T_Deprecated", "A status indicating retained compatibility without preferred new use."),
    atomic("T_Working", "A status indicating an unresolved or provisional state."),
    atomic("T_Accepted", "A status indicating inclusion in the current consolidated model."),
    atomic("T_Open", "A status indicating unresolved work."),
    atomic("T_Planned", "A status indicating intended future implementation."),
    atomic("T_Implemented", "A status indicating an existing executable implementation."),
    atomic("T_Intersection", "A composition operator requiring all argument properties."),
    atomic("T_Composition", "A composition operator forming a concept from argument concepts."),
    atomic("T_Sequence", "A composition operator imposing ordered execution."),
]

derived_tokens = [
    derived("T_CognitiveSystem", "T_System", "T_Cognition", "T_Agent", operator="T_Intersection"),
    derived("T_WorldModel", "T_Model", "T_Knowledge", "T_Environment", "T_Objective"),
    derived("T_ObjectiveFunction", "T_Objective", "T_Function", "T_Evaluation"),
    derived("T_WorkingMemory", "T_Memory", "T_State", "T_Time"),
    derived("T_LongTermMemory", "T_Memory", "T_Experience", "T_Structure"),
    derived("T_PartialSerialization", "T_Serialization", "T_Model", "T_Constraint", "T_Communication"),
    derived("T_Deserialization", "T_Transformation", "T_Communication", "T_Information", "T_Structure"),
    derived("T_ModelIntegration", "T_Process", "T_Information", "T_Model", "T_Optimization"),
    derived("T_ClarificationRequest", "T_Communication", "T_Conflict", "T_Information", "T_Question"),
    derived("T_ModelConflictResolution", "T_Process", "T_Conflict", "T_Optimization", "T_Model"),
    derived("T_Consolidation", "T_Process", "T_Memory", "T_Transformation", "T_Optimization"),
    derived("T_GlobalEvaluation", "T_Evaluation", "T_Information", "T_Objective", "T_Function"),
    derived("T_FunctionalSelf", "T_Model", "T_Identity", "T_Agent", "T_Time", "T_Objective"),
    derived("T_MetaArchitect", "T_System", "T_Optimization", "T_Architecture", "T_Algorithm", "T_NeuralNetwork"),
    derived("T_CognitiveLineage", "T_Collection", "T_Cognition", "T_Lineage", "T_Identity"),
    derived("T_ResearchState", "T_State", "T_Knowledge", "T_Architecture", "T_History"),
    derived("T_ConsolidationRecord", "T_Document", "T_Transformation", "T_State", "T_History"),
    derived("T_Principle", "T_Knowledge", "T_Constraint", "T_Architecture"),
    derived("T_Hypothesis", "T_Model", "T_Uncertainty", "T_Evidence"),
    derived("T_ArchitectureDecision", "T_Architecture", "T_Evaluation", "T_Action"),
    derived("T_OpenQuestion", "T_Question", "T_Uncertainty", "T_Knowledge"),
    derived("T_RoadmapItem", "T_Action", "T_Time", "T_Objective"),
    derived("T_Chapter", "T_Document", "T_Structure", "T_Knowledge"),
    derived("T_Section", "T_Document", "T_Structure"),
    derived("T_ContentBlock", "T_Document", "T_Information", "T_Structure"),
    derived("T_ChangeProposal", "T_Document", "T_Action", "T_Transformation"),
    derived("T_SemanticMergeReport", "T_Document", "T_History", "T_Conflict"),
]

write(
    "tokens.yaml",
    {
        "kind": "T_Collection",
        "tokens": atomic_tokens + derived_tokens,
        "optimization_goal": "Reduce the Atomic Token set while preserving or increasing expressive power.",
    },
)

principles = [
    ("P_001", "Architecture over component complexity", "Prefer improved organization of existing components over increasing the complexity of individual components."),
    ("P_002", "Evolution over replacement", "Construct independently useful stages that create evidence and infrastructure for deeper integration."),
    ("P_003", "Best next step", "Choose the next architectural change by practical utility, engineering cost, risk, and the number of future options it opens."),
    ("P_004", "Biological evidence", "Treat durable biological solutions as strong architectural candidates, not as proof of engineering optimality."),
    ("P_005", "State and computation separation", "Keep persistent user or research state independent from replaceable computational models."),
    ("P_006", "Token semantic stability", "Never redefine the semantic identity of a Token; introduce a new Token when the meaning changes."),
    ("P_007", "Atomic reduction", "Judge language maturation partly by reduction of the Atomic Token set without loss of expressive power."),
    ("P_008", "Single history mechanism", "Use Git as the only version-history mechanism; do not reproduce repository history inside Research State."),
    ("P_009", "Semantic transition record", "Store only the latest semantic consolidation record in each version of Research State; Git distributes prior records across commits."),
    ("P_010", "Canonical project language", "Write all project artifacts in English while permitting design dialogue in any language."),
    ("P_011", "Architectural primacy", "Engineer fundamental computational mechanisms before directly engineering higher-level behavior."),
    ("P_012", "Communication decomposition", "Model communication as partial serialization, deserialization, and integration into the recipient's own model."),
    ("P_013", "Generated documentation", "Treat human-readable documents as partial serializations generated from canonical Research State."),
    ("P_014", "Delayed deep integration", "Use current components in a working system before attempting a tighter integrated representation."),
    ("P_015", "State recovery", "Research State and generated documentation must permit work to resume after context loss with minimal reconstruction."),
]
write(
    "principles.yaml",
    {
        "kind": "T_Collection",
        "principles": [
            {
                "id": pid,
                "kind": "T_Principle",
                "title": title,
                "statement": statement,
                "status": "T_Accepted",
            }
            for pid, title, statement in principles
        ],
    },
)

hypotheses = [
    ("H_001", "Long-term cognitive capability depends more on knowledge organization than on isolated inference power.", 0.82, ["A system with stable inference but improved memory organization should improve on longitudinal tasks."], ["Longitudinal capability scales only with inference-model capability after controlling for memory organization."]),
    ("H_002", "No finite universal world model exists; world models are optimized for objective-limited classes of cognitive systems.", 0.90, ["Predator, herbivore, scientist, and artist models preserve different distinctions in the same environment."], ["One finite representation is shown to dominate all alternatives across every objective class."]),
    ("H_003", "Biological long-term memory is functionally lossy because integration and future utility are optimized over archival fidelity.", 0.78, ["Reconstructive recall and systematic loss coexist with effective action."], ["Loss is fully explained by storage limits and provides no functional advantage."]),
    ("H_004", "Most new experience first changes importance, utility, confidence, and activation weights before changing architecture.", 0.85, ["Local reweighting is cheaper and more frequent than structural reorganization."], ["Each significant experience deterministically rewrites architecture."]),
    ("H_005", "Large architectural consolidation is an iterative search process, not a deterministic transformation from changed weights.", 0.88, ["The optimal reorganization cannot be known before candidate evaluation."], ["A general closed-form optimal restructuring function is demonstrated."]),
    ("H_006", "A trainable integrated multichannel evaluation mechanism is a prerequisite for a persistent functional Self.", 0.72, ["Cross-domain decisions require comparison on a common learned scale."], ["Stable self-continuity and goal selection emerge without any integrated evaluation mechanism."]),
    ("H_007", "Social, psychological, ethical, political, and emotional phenomena can emerge from mature cognitive architecture rather than separate hard-coded subsystems.", 0.62, ["Higher-level behavior in biological systems emerges from interacting lower-level mechanisms."], ["A target phenomenon requires an irreducible independent module in every viable architecture."]),
    ("H_008", "For strongly integrated distributed memories, dialogue is the maximum generally viable form of experience transfer; direct Merge is not well-defined.", 0.86, ["An experience derives meaning from system-wide context that cannot be inserted locally into another model."], ["Arbitrary mature cognitive states can be merged without destructive interference or identity loss."]),
    ("H_009", "A significant book or lecture changes the integrated evaluation system and therefore future attention, questions, and learning direction.", 0.84, ["Readers retain changed judgments after explicit details are forgotten."], ["All durable effects are explainable as retrieval of stored propositions alone."]),
    ("H_010", "A trainable meta-architect can improve practical task decomposition between neural and algorithmic computation using current technology.", 0.91, ["Task descriptors and observed utility provide a direct supervised or bandit learning signal."], ["No stable task features predict executor performance better than random allocation."]),
    ("H_011", "A small set of diverse cognitive lineages with champion cloning inside each lineage balances commercial efficiency and population resilience.", 0.80, ["Colony-like biological strategies combine specialization and diversity."], ["A single globally cloned champion remains robust under broad unforeseen environmental changes."]),
    ("H_012", "A holographic-style representation transformation may make memory, world model, and some higher-level forces different projections of one integrated state.", 0.55, ["One representation could remove explicit subsystems by making their behavior emergent."], ["Every candidate integrated representation performs worse than explicit modular decomposition."]),
    ("H_013", "Shared cognitive background contains more information than the new serialized message by definition and is the main source of communication compression.", 0.96, ["Experts communicate complex structures through very short signals."], ["Message size alone predicts communicated meaning independently of shared background."]),
    ("H_014", "What is commonly called a universal human world model is largely the objective-driven model of a scientist.", 0.75, ["Scientific cognition optimizes prediction, explanation, reproducibility, and consistency."], ["The scientific model is optimal for all biological, artistic, social, and engineering objectives."]),
    ("H_015", "An efficient internal cognitive language will probably differ substantially from natural English and may use dense context-dependent symbols.", 0.67, ["Natural language is optimized for communication among non-identical humans, not internal integrated storage."], ["Natural English remains optimal for integrated memory, computation, and communication across mature systems."]),
]
write(
    "hypotheses.yaml",
    {
        "kind": "T_Collection",
        "hypotheses": [
            {
                "id": hid,
                "kind": "T_Hypothesis",
                "statement": statement,
                "status": "T_Working",
                "confidence": confidence,
                "evidence": evidence,
                "falsifiers": falsifiers,
            }
            for hid, statement, confidence, evidence, falsifiers in hypotheses
        ],
    },
)

architectures = [
    {
        "id": "A_001",
        "kind": "T_ArchitectureDecision",
        "title": "Research State development loop",
        "status": "T_Implemented",
        "summary": "Discussion produces reviewed semantic changes to canonical T_ResearchState, from which documentation is generated.",
        "relations": [
            "Discussion -> T_ChangeProposal",
            "T_ChangeProposal -> T_ConsolidationRecord",
            "T_ConsolidationRecord -> T_ResearchState",
            "T_ResearchState -> T_Document",
        ],
    },
    {
        "id": "A_002",
        "kind": "T_ArchitectureDecision",
        "title": "Memory and consolidation pipeline",
        "status": "T_Implemented",
        "summary": "T_WorkingMemory receives experience; T_LongTermMemory retains functionally useful state; T_Consolidation performs lossy compression and iterative architectural search.",
        "relations": [
            "T_Experience -> T_WorkingMemory",
            "T_WorkingMemory -> T_Consolidation",
            "T_Consolidation -> T_LongTermMemory",
            "T_LongTermMemory -> T_WorldModel",
        ],
    },
    {
        "id": "A_003",
        "kind": "T_ArchitectureDecision",
        "title": "Communication pipeline",
        "status": "T_Implemented",
        "summary": "Communication is decomposed into T_PartialSerialization, T_Deserialization, T_ModelIntegration, clarification, and T_ModelConflictResolution.",
        "relations": [
            "T_WorldModel -> T_PartialSerialization",
            "T_PartialSerialization -> T_Channel",
            "T_Channel -> T_Deserialization",
            "T_Deserialization -> T_ModelIntegration",
        ],
    },
    {
        "id": "A_004",
        "kind": "T_ArchitectureDecision",
        "title": "Integrated evaluation and functional Self",
        "status": "T_Implemented",
        "summary": "A trainable T_GlobalEvaluation compares heterogeneous channels and supports continuity, goals, and causal attribution in T_FunctionalSelf.",
        "relations": [
            "T_Observation -> T_GlobalEvaluation",
            "T_GlobalEvaluation -> T_ObjectiveFunction",
            "T_ObjectiveFunction -> T_Action",
            "T_Action -> T_FunctionalSelf",
        ],
    },
    {
        "id": "A_005",
        "kind": "T_ArchitectureDecision",
        "title": "Hybrid computation meta-architecture",
        "status": "T_Implemented",
        "summary": "T_MetaArchitect allocates task operations among T_Algorithm, T_NeuralNetwork, and hybrid pipelines and learns from observed utility.",
        "relations": [
            "T_Question -> T_MetaArchitect",
            "T_MetaArchitect -> T_ArchitectureDecision",
            "T_ArchitectureDecision -> T_Algorithm",
            "T_ArchitectureDecision -> T_NeuralNetwork",
        ],
    },
    {
        "id": "A_006",
        "kind": "T_ArchitectureDecision",
        "title": "Cognitive lineage population",
        "status": "T_Implemented",
        "summary": "Maintain multiple diverse T_CognitiveLineage classes while cloning high-performing systems within each lineage.",
        "relations": [
            "T_CognitiveLineage -> T_CognitiveSystem",
            "T_Evaluation -> T_CognitiveLineage",
            "T_Communication -> T_CognitiveLineage",
        ],
    },
]
write(
    "architecture.yaml",
    {
        "kind": "T_Collection",
        "architectures": architectures,
    },
)

questions = [
    ("Q_001", "Which minimal Atomic Token set preserves the full expressive power of Research State?", "high"),
    ("Q_002", "Which integrated representation can combine memory and model without catastrophic interference?", "high"),
    ("Q_003", "How should consolidation candidates be generated and evaluated over long horizons?", "high"),
    ("Q_004", "Which measurable thresholds should trigger architectural search rather than local reweighting?", "high"),
    ("Q_005", "How can a global evaluation network be trained without freezing accidental initial values?", "high"),
    ("Q_006", "Which features best predict the optimal neural-algorithmic task split?", "high"),
    ("Q_007", "How can communication preserve productive model diversity while reducing unnecessary conflict?", "medium"),
    ("Q_008", "What is the smallest useful number of cognitive lineages under realistic environmental uncertainty?", "medium"),
    ("Q_009", "Can reading be evaluated by changes in learning direction rather than immediate recall?", "medium"),
    ("Q_010", "How can semantic consolidation be reviewed and reproduced without storing private raw dialogue?", "high"),
    ("Q_011", "Which parts of higher-level social and emotional behavior fail to emerge and require explicit mechanisms?", "medium"),
    ("Q_012", "Can a mature cognitive state be cloned onto new hardware while preserving identity continuity?", "medium"),
]
write(
    "questions.yaml",
    {
        "kind": "T_Collection",
        "questions": [
            {
                "id": qid,
                "kind": "T_OpenQuestion",
                "title": text,
                "status": "T_Open",
                "priority": priority,
            }
            for qid, text, priority in questions
        ],
    },
)

roadmap = [
    ("R_001", "Formal Research State and restricted YAML toolchain", "T_Implemented", 1),
    ("R_002", "Generated semantic HTML documentation", "T_Implemented", 2),
    ("R_003", "Working and long-term memory prototype with lossy consolidation", "T_Implemented", 3),
    ("R_004", "Communication, clarification, and conflict prototype", "T_Implemented", 4),
    ("R_005", "Trainable integrated multichannel evaluator", "T_Implemented", 5),
    ("R_006", "Trainable neural-algorithmic meta-architect", "T_Implemented", 6),
    ("R_007", "Cognitive lineage diversity manager", "T_Implemented", 7),
    ("R_008", "Longitudinal experiments with persistent agents", "T_Planned", 8),
    ("R_009", "Integrated memory-model representation experiments", "T_Planned", 9),
    ("R_010", "Self-hosting Research State rules and generator descriptions", "T_Planned", 10),
]
write(
    "roadmap.yaml",
    {
        "kind": "T_Collection",
        "roadmap": [
            {
                "id": rid,
                "kind": "T_RoadmapItem",
                "title": title,
                "status": status,
                "order": order,
            }
            for rid, title, status, order in roadmap
        ],
    },
)

write(
    "consolidation.yaml",
    {
        "kind": "T_ConsolidationRecord",
        "latest": {
            "id": "CR_001",
            "kind": "T_ConsolidationRecord",
            "timestamp": "2026-07-28T00:00:00+00:00",
            "summary": "Initial consolidated implementation of the long-lived cognitive systems project.",
            "semantic_change": True,
            "inputs": ["Extended human-model design dialogue"],
            "changed_roles": [
                "tokens",
                "principles",
                "hypotheses",
                "architecture",
                "questions",
                "roadmap",
                "chapters",
            ],
            "alternatives": [
                "Document-first development without canonical Research State",
                "Unrestricted YAML",
                "One universal cognitive model",
            ],
            "rationale": "The selected architecture maximizes current practical utility while creating reusable infrastructure for deeper future integration.",
            "open_questions": ["Q_001", "Q_002", "Q_003", "Q_005", "Q_006"],
        },
    },
)

write(
    "manifest.yaml",
    {
        "kind": "T_ResearchState",
        "title": "Architectural Evolution of Long-Lived Cognitive Systems",
        "canonical_language": "en",
        "files": {
            "tokens": "tokens.yaml",
            "principles": "principles.yaml",
            "hypotheses": "hypotheses.yaml",
            "architecture": "architecture.yaml",
            "questions": "questions.yaml",
            "roadmap": "roadmap.yaml",
            "consolidation": "consolidation.yaml",
            "chapters": "chapters.yaml",
            "content_directory": "content",
            "documentation_output": "generated",
        },
    },
)

print(f"Bootstrapped state in {STATE}")

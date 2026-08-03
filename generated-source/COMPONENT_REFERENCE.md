# Component Reference

## External Input

- ID: `C_EXT_INPUT`
- Kind: `external`
- Roles: `observation_source`

## Transformer

- ID: `C_TRANSFORMER`
- Kind: `subsystem`
- Roles: `semantic_reasoning_engine`, `semantic_teacher`

## Associative Memory

- ID: `C_ASSOC_MEMORY`
- Kind: `subsystem`
- Roles: `contextual_retriever`, `semantic_learner`

## Memory State

- ID: `C_MEMORY_STATE`
- Kind: `state`
- Roles: `persistent_and_dynamic_memory_state`

## Memory Vector

- ID: `C_MEMORY_VECTOR`
- Kind: `interface`
- Roles: `read_result`, `transformer_conditioning`

## Semantic Representation

- ID: `C_SEM_REP`
- Kind: `data`
- Roles: `canonical_update_input`

## Semantic Feedback Learning Pipeline

- ID: `C_SFL_PIPELINE`
- Kind: `process`
- Roles: `self_learning`, `learning_coordination`

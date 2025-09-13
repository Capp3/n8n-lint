# 📋 Implementation Plan - Validation Separation Enhancement

**Date:** 2025-09-13  
**Task Level:** Level 2 (Simple Enhancement)  
**Complexity:** Modify existing validation logic to separate general and deep validation  
**Estimated Time:** 2-3 hours

---

## 🎯 **OBJECTIVE**

Separate validation into two distinct modes:

1. **General Validation** (`validate` command) - Fast structure validation for common node properties
2. **Deep Validation** (`deep-validate` command) - Schema-based validation for specific node types

---

## 📊 **CURRENT STATE ANALYSIS**

### Existing Validation Logic

- ✅ **Workflow Structure Validation**: Already validates `nodes` and `connections` fields
- ✅ **Node Validation**: Currently validates against specific node schemas
- ✅ **CLI Structure**: Supports multiple commands with proper argument handling
- ✅ **Error Reporting**: Comprehensive error logging and reporting system

### Common Node Properties (All Node Types)

Based on sample workflow analysis:

- ✅ `id` - Unique node identifier
- ✅ `name` - Human-readable node name
- ✅ `type` - Node type identifier
- ✅ `typeVersion` - Version of the node type
- ✅ `position` - X,Y coordinates for UI placement

---

## 🏗️ **IMPLEMENTATION STRATEGY**

### Phase 1: Create General Node Validation Rule

**Estimated Time:** 45 minutes

#### 1.1 Create General Node Validation Rule

- **File**: `src/n8n_lint/core/validator.py`
- **Action**: Create new `GeneralNodeValidationRule` class
- **Properties to Validate**:
  - `id`: Required string
  - `name`: Required string
  - `type`: Required string
  - `typeVersion`: Required number
  - `position`: Required array with 2 numbers
- **Error Messages**: Clear, specific error messages for each missing property

#### 1.2 Update Validation Engine

- **File**: `src/n8n_lint/core/validator.py`
- **Action**: Modify `ValidationEngine` class
- **Changes**:
  - Add `validation_mode` parameter (general/deep)
  - Create separate validation methods for each mode
  - Update `_validate_node` to use appropriate validation rules

### Phase 2: Refactor CLI Commands

**Estimated Time:** 30 minutes

#### 2.1 Modify Existing `validate` Command

- **File**: `src/n8n_lint/cli/main.py`
- **Action**: Update `validate` function to use general validation mode
- **Changes**:
  - Add `--deep` flag for backward compatibility
  - Set default validation mode to "general"
  - Update help text to reflect new behavior

#### 2.2 Add New `deep-validate` Command

- **File**: `src/n8n_lint/cli/main.py`
- **Action**: Create new `deep_validate` function
- **Features**:
  - Same parameters as `validate` command
  - Uses deep validation mode (schema-based)
  - Keep undocumented as requested

### Phase 3: Update Core Validation Logic

**Estimated Time:** 60 minutes

#### 3.1 Create Validation Mode Enum

- **File**: `src/n8n_lint/core/validator.py`
- **Action**: Add `ValidationMode` enum
- **Values**: `GENERAL`, `DEEP`

#### 3.2 Refactor Validation Engine

- **File**: `src/n8n_lint/core/validator.py`
- **Action**: Update `ValidationEngine` class
- **Changes**:
  - Add `validation_mode` parameter to constructor
  - Create `_validate_node_general()` method
  - Create `_validate_node_deep()` method
  - Update `_validate_node()` to route to appropriate method

#### 3.3 Update Main Validation Function

- **File**: `src/n8n_lint/core/validator.py`
- **Action**: Modify `validate_workflow_file()` function
- **Changes**:
  - Add `validation_mode` parameter
  - Pass mode to ValidationEngine constructor
  - Update function signature and documentation

### Phase 4: Update Tests

**Estimated Time:** 45 minutes

#### 4.1 Update Existing Tests

- **File**: `tests/test_cli.py`
- **Action**: Update CLI tests to handle new validation modes
- **Changes**:
  - Update `test_validate_command_*` tests
  - Add tests for `deep-validate` command
  - Ensure backward compatibility tests pass

#### 4.2 Update Validator Tests

- **File**: `tests/test_validator.py`
- **Action**: Update validator tests for new validation modes
- **Changes**:
  - Test general validation mode
  - Test deep validation mode
  - Test error handling for both modes

### Phase 5: Integration Testing

**Estimated Time:** 30 minutes

#### 5.1 Test Both Validation Modes

- **Action**: Comprehensive testing of both commands
- **Test Cases**:
  - Valid workflow with both modes
  - Invalid workflow with missing general properties
  - Invalid workflow with missing schema-specific properties
  - Performance comparison between modes

#### 5.2 Update Documentation

- **Action**: Update internal documentation only
- **Files**: Keep `deep-validate` out of public documentation as requested
- **Changes**: Update code comments and docstrings

---

## 🔧 **TECHNICAL IMPLEMENTATION DETAILS**

### General Node Validation Rule

```python
class GeneralNodeValidationRule(ValidationRule):
    """Validates common properties present in all n8n nodes."""

    def __init__(self):
        super().__init__("general_node", "Validates common node properties")

    def validate(self, node: dict, context: dict) -> list[ValidationError]:
        """Validate common node properties."""
        errors = []

        # Required properties for all nodes
        required_props = {
            'id': str,
            'name': str,
            'type': str,
            'typeVersion': (int, float),
            'position': list
        }

        # Validate each required property
        for prop, expected_type in required_props.items():
            if prop not in node:
                errors.append(ValidationError(
                    message=f"Required property '{prop}' is missing",
                    severity="error",
                    node_type=context.get("node_type"),
                    property_path=prop,
                    # ... other parameters
                ))
            elif not isinstance(node[prop], expected_type):
                errors.append(ValidationError(
                    message=f"Property '{prop}' must be {expected_type.__name__}",
                    severity="error",
                    node_type=context.get("node_type"),
                    property_path=prop,
                    # ... other parameters
                ))

        # Validate position array specifically
        if 'position' in node and isinstance(node['position'], list):
            if len(node['position']) != 2:
                errors.append(ValidationError(
                    message="Property 'position' must be an array with exactly 2 numbers",
                    severity="error",
                    node_type=context.get("node_type"),
                    property_path="position",
                    # ... other parameters
                ))

        return errors
```

### CLI Command Structure

```python
@app.command()
def validate(
    file_path: Path = FILE_PATH_ARG,
    deep: bool = typer.Option(False, "--deep", help="Use deep validation (schema-based)"),
    # ... other existing parameters
):
    """Validate an n8n workflow JSON file with general structure validation."""

    validation_mode = ValidationMode.DEEP if deep else ValidationMode.GENERAL

    exit_code = validate_workflow_file(
        file_path=file_path,
        validation_mode=validation_mode,
        # ... other parameters
    )

@app.command()
def deep_validate(
    file_path: Path = FILE_PATH_ARG,
    # ... same parameters as validate
):
    """Perform deep validation with schema-based node type checking."""

    exit_code = validate_workflow_file(
        file_path=file_path,
        validation_mode=ValidationMode.DEEP,
        # ... other parameters
    )
```

---

## 📋 **IMPLEMENTATION CHECKLIST**

### Phase 1: General Validation Rule

- [ ] Create `GeneralNodeValidationRule` class
- [ ] Implement property validation logic
- [ ] Add position array validation
- [ ] Test rule independently

### Phase 2: CLI Commands

- [ ] Add `ValidationMode` enum
- [ ] Update `validate` command with `--deep` flag
- [ ] Create `deep-validate` command
- [ ] Update help text and documentation

### Phase 3: Core Logic Updates

- [ ] Update `ValidationEngine` constructor
- [ ] Create `_validate_node_general()` method
- [ ] Create `_validate_node_deep()` method
- [ ] Update `_validate_node()` routing logic
- [ ] Update `validate_workflow_file()` function signature

### Phase 4: Testing

- [ ] Update CLI tests for both commands
- [ ] Update validator tests for both modes
- [ ] Test backward compatibility
- [ ] Test error handling in both modes

### Phase 5: Integration

- [ ] Test with sample workflows
- [ ] Performance comparison testing
- [ ] Update internal documentation
- [ ] Final validation and cleanup

---

## 🎯 **SUCCESS CRITERIA**

### Functional Requirements

- ✅ **General Validation**: `validate` command checks common node properties
- ✅ **Deep Validation**: `deep-validate` command performs schema-based validation
- ✅ **Backward Compatibility**: Existing functionality preserved with `--deep` flag
- ✅ **Performance**: General validation significantly faster than deep validation
- ✅ **Error Reporting**: Clear, specific error messages for both modes

### Technical Requirements

- ✅ **Code Quality**: All tests pass, no linting issues
- ✅ **Documentation**: Internal docs updated, `deep-validate` kept undocumented
- ✅ **CLI Interface**: Both commands work with existing parameters
- ✅ **Error Handling**: Proper error handling for both validation modes

### User Experience

- ✅ **Fast Validation**: General validation completes quickly
- ✅ **Detailed Validation**: Deep validation provides comprehensive checking
- ✅ **Clear Commands**: Intuitive command names and help text
- ✅ **Consistent Interface**: Same parameters work for both commands

---

## 🚀 **DEPLOYMENT CONSIDERATIONS**

### Version Impact

- **Minor Version Bump**: This is an enhancement, not a breaking change
- **Backward Compatibility**: Existing usage patterns continue to work
- **New Feature**: `deep-validate` command adds new functionality

### Documentation Updates

- **Public Docs**: Update `validate` command documentation
- **Keep Undocumented**: `deep-validate` command not added to public docs
- **Internal Docs**: Update code comments and docstrings

### Testing Strategy

- **Unit Tests**: Test both validation modes independently
- **Integration Tests**: Test CLI commands with various workflows
- **Performance Tests**: Verify general validation is faster
- **Regression Tests**: Ensure existing functionality works

---

**Estimated Total Time:** 3 hours  
**Risk Level:** Low (well-contained changes)  
**Dependencies:** None (self-contained enhancement)  
**Testing Requirements:** Unit tests, integration tests, performance validation

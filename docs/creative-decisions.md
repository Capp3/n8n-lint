# Creative Phase Design Decisions

## Overview

This document records the design decisions made during the creative phase for the n8n JSON Linter project. All decisions were made based on user requirements and technical constraints.

## Creative Phase 1: Schema Management Strategy

### Problem Statement

Design a schema management system that combines manual creation with CLI import capabilities, using JSON Schema format for maximum compatibility.

### Options Considered

#### Option 1: Directory-Based Schema Loading

- **Pros**: Simple file-based organization, easy to add new schemas, clear separation of concerns
- **Cons**: No schema validation on load, potential naming conflicts, no metadata about schemas
- **Complexity**: Low
- **Implementation Time**: 2-3 hours

#### Option 2: Registry-Based Schema Management

- **Pros**: Schema validation and metadata, conflict resolution, better error handling
- **Cons**: More complex implementation, registry file maintenance, potential registry corruption
- **Complexity**: Medium
- **Implementation Time**: 4-6 hours

#### Option 3: Hybrid Schema System

- **Pros**: Best of both approaches, CLI validation and import, automatic discovery with metadata
- **Cons**: Most complex implementation, multiple files to maintain, higher learning curve
- **Complexity**: High
- **Implementation Time**: 6-8 hours

### Decision

**Chosen**: Option 3 - Hybrid Schema System

**Rationale**: Provides the flexibility of directory-based storage with the robustness of registry management. The CLI import capability addresses the extensibility requirement while maintaining JSON Schema compatibility.

### Implementation Plan

1. Create `schemas/` directory structure
2. Implement `schemas/registry.json` for metadata
3. Add CLI command `n8n_lint import-schema <file>`
4. Schema validation on import
5. Automatic discovery with fallback to registry

## Creative Phase 2: Validation Engine Architecture

### Problem Statement

Design a validation engine with configurable strictness, comprehensive error collection, and balanced performance.

### Options Considered

#### Option 1: Rule-Based Validation Engine

- **Pros**: Highly modular and extensible, easy to add new validation rules, clear separation of concerns
- **Cons**: More complex architecture, potential performance overhead, rule coordination complexity
- **Complexity**: Medium
- **Implementation Time**: 6-8 hours

#### Option 2: Pipeline-Based Validation Engine

- **Pros**: Clear data flow, easy to add new stages, good performance characteristics
- **Cons**: Less flexible than rule-based, harder to skip stages, potential bottlenecks
- **Complexity**: Medium
- **Implementation Time**: 4-6 hours

#### Option 3: Visitor Pattern Validation Engine

- **Pros**: Natural fit for tree structures, easy to add new node types, clean separation of traversal and validation
- **Cons**: More complex for simple validations, potential performance overhead, learning curve for developers
- **Complexity**: High
- **Implementation Time**: 8-10 hours

### Decision

**Chosen**: Option 1 - Rule-Based Validation Engine

**Rationale**: Provides the best balance of extensibility and maintainability. The modular approach allows for easy addition of new validation rules and supports the configurable strictness requirement.

### Implementation Plan

1. Create base `ValidationRule` abstract class
2. Implement specific rules (RequiredProperty, TypeValidation, etc.)
3. Create `ValidationEngine` to coordinate rules
4. Add configuration for strictness levels
5. Implement error aggregation system

## Creative Phase 3: Error Aggregation Strategy

### Problem Statement

Design an error system with detailed categories, full context reporting, and node-based grouping with severity prioritization.

### Options Considered

#### Option 1: Hierarchical Error Structure

- **Pros**: Natural organization, easy to navigate, clear hierarchy, good for reporting
- **Cons**: Complex data structure, potential memory overhead, harder to implement
- **Complexity**: High
- **Implementation Time**: 6-8 hours

#### Option 2: Flat Error List with Grouping

- **Pros**: Simple data structure, easy to implement, good performance, flexible sorting
- **Cons**: Less intuitive organization, grouping logic complexity, potential duplicate information
- **Complexity**: Medium
- **Implementation Time**: 4-6 hours

#### Option 3: Hybrid Error System

- **Pros**: Best of both approaches, simple storage, rich presentation, good performance
- **Cons**: More complex implementation, multiple data structures, potential inconsistency
- **Complexity**: Medium-High
- **Implementation Time**: 5-7 hours

### Decision

**Chosen**: Option 3 - Hybrid Error System

**Rationale**: Provides the performance benefits of flat storage with the rich presentation capabilities of hierarchical organization. Supports both detailed error reporting and efficient processing.

### Implementation Plan

1. Create `ValidationError` class with full context
2. Implement `ErrorAggregator` for collection and grouping
3. Add severity-based sorting and filtering
4. Create reporting formatters for console and JSON
5. Implement node-based grouping with summaries

## Creative Phase 4: JSON Parsing Strategy

### Problem Statement

Design a JSON parsing system for small files with streaming node processing and intelligent error recovery.

### Options Considered

#### Option 1: Standard JSON Parser with Post-Processing

- **Pros**: Simple implementation, reliable parsing, good error messages, fast for small files
- **Cons**: Limited error recovery, no streaming capabilities, memory usage for large files
- **Complexity**: Low
- **Implementation Time**: 2-3 hours

#### Option 2: Streaming JSON Parser

- **Pros**: Memory efficient, true streaming, better error recovery, scalable design
- **Cons**: Complex implementation, potential parsing errors, more testing required
- **Complexity**: High
- **Implementation Time**: 8-10 hours

#### Option 3: Hybrid Parser with Error Recovery

- **Pros**: Good balance of simplicity and features, error recovery capabilities, helpful error messages
- **Cons**: Moderate complexity, error recovery logic, testing complexity
- **Complexity**: Medium
- **Implementation Time**: 4-6 hours

### Decision

**Chosen**: Option 3 - Hybrid Parser with Error Recovery

**Rationale**: Provides the reliability of standard JSON parsing with the added value of error recovery and suggestions. Meets the requirement for small file handling while providing helpful error messages.

### Implementation Plan

1. Use standard JSON parser for reliability
2. Add error recovery for common issues (missing commas, quotes)
3. Implement error suggestion system
4. Add node-by-node processing for validation
5. Create helpful error messages with context

## Creative Phase 5: CLI Integration Strategy

### Problem Statement

Design a CLI with direct validation, Rich formatting with plain text fallback, and detailed exit codes.

### Options Considered

#### Option 1: Single Command with Flags

- **Pros**: Simple command structure, easy to remember, clear purpose, minimal complexity
- **Cons**: Limited extensibility, hard to add new features, single responsibility
- **Complexity**: Low
- **Implementation Time**: 2-3 hours

#### Option 2: Multi-Command Structure

- **Pros**: Extensible design, clear command separation, easy to add new commands, better help system
- **Cons**: More complex implementation, longer command names, potential confusion
- **Complexity**: Medium
- **Implementation Time**: 4-6 hours

#### Option 3: Hybrid Command Structure

- **Pros**: Best of both approaches, simple for basic use, extensible for advanced features, clear command hierarchy
- **Cons**: Moderate complexity, command parsing logic, help system complexity
- **Complexity**: Medium
- **Implementation Time**: 3-5 hours

### Decision

**Chosen**: Option 3 - Hybrid Command Structure

**Rationale**: Provides the simplicity of direct validation for common use cases while maintaining extensibility for advanced features like schema import.

### Implementation Plan

1. Implement direct validation as default command
2. Add `--plain-text` flag for Rich formatting
3. Add `--output json` for machine-readable output
4. Implement detailed exit codes
5. Add subcommands for advanced features (import-schema)

## Summary

All creative phase design decisions have been completed with detailed analysis of options, clear rationale for choices, and comprehensive implementation plans. The decisions provide a solid foundation for the implementation phase while maintaining flexibility for future enhancements.

**Total Implementation Time Estimate**: 20-30 hours across all components
**Complexity Level**: Medium-High (appropriate for Level 3 task)
**Risk Level**: Low (all decisions based on proven patterns and user requirements)

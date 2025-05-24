# Architectural Review: Simple Stock Strategy Backtester (S3B)
## Audit Date: 2025-05-24

---

## RESOLVED ISSUES

All previously documented architectural directives (TEST-001, LOG-001, TEST-002) were confirmed as RESOLVED as of 2025-05-20. The TEST-003 issue identified on 2025-05-23 has been RESOLVED. The DESIGN-001 issue related to feature generation orchestration identified on 2025-05-23 has been RESOLVED. The TEST-004 issue related to suboptimal test implementation has been RESOLVED. The IMPORT-001 issue related to non-standard import practices in test_backtester.py has been RESOLVED. The TEST-005 issue related to imprecise test assertions in backtester tests has been RESOLVED as of 2025-05-24. The CODE-001 issue related to duplicate NamedTuple definition in backtester.py has been RESOLVED as of 2025-05-24. The TEST-008 issue related to standalone integration test has been RESOLVED as of 2025-05-24. The DOC-003 issue related to misplaced documentation file has been RESOLVED as of 2025-05-24. The TEST-009 issue related to duplicate test files for metrics.py has been RESOLVED as of 2025-05-24. Refer to `resolved_issues.md` for details.

---

## PARTIALLY RESOLVED/REGRESSED ISSUES

_None at this time._

---

## NEW CRITICAL FLAWS (Identified This Audit)

**TEST-006:** Test Code Quality Degradation in `tests/test_data_loader.py`. The test file contained two nearly identical, extensive sets of tests: one for the legacy `fetch` function and one for the primary `fetch_data` function. This violated the DRY (Don't Repeat Yourself) principle, leading to significant code duplication and increased maintenance overhead.

**Flaw Impact:** Medium-High - Any change to the data loading logic required updating two sets of tests, increasing the risk of them becoming inconsistent. It bloated the test suite and made it harder to read and maintain.

**Root Cause:** When `fetch_data` was introduced as the primary function, its tests were created by copy-pasting the tests for the `fetch` function, without refactoring to eliminate the redundancy.

**Mandated Solution:** 
1. ✅ **RESOLVED** - Retained the comprehensive test suite for the primary `fetch_data` function
2. ✅ **RESOLVED** - Removed all redundant tests for the `fetch` function (e.g., `test_fetch_validates_ticker`, `test_fetch_validates_period`, `test_fetch_caching`, etc.)
3. ✅ **RESOLVED** - Kept only the single, targeted test `test_fetch_delegates_to_fetch_data` to ensure the wrapper correctly calls the primary function

**Systemic Prevention:** Code review checklists must include a point to specifically check for test code duplication when a legacy API is being wrapped by a new one.

**DOC-001:** Documentation Veracity Failure in `docs/tasks.md`. Tasks 20, 21, and 22 in the Backtester Module were marked as incomplete [ ] despite being fully implemented in `src/backtester.py` with comprehensive test coverage. This documentation inconsistency violated the Core Engineering Principle #6 requiring that documentation accurately reflects the codebase state.

**Flaw Impact:** High - Misleads developers about implementation status, undermines documentation trustworthiness, and violates the explicit directive that documentation must be a truthful representation of the codebase.

**Root Cause:** Task completion status was not updated when implementation was completed, indicating insufficient synchronization between code implementation and documentation maintenance.

**Mandated Solution:** 
1. ✅ **RESOLVED** - Updated `docs/tasks.md` to mark Tasks 20, 21, 22 as complete with detailed completion descriptions
2. ✅ **RESOLVED** - Updated progress summary to reflect correct completion count (22/30 = 73% vs 19/30 = 63%)
3. **REQUIRED** - Implement systemic prevention measures to ensure documentation-code synchronization

**Systemic Prevention:** Mandatory pre-commit/CI checks must verify that:
- Task completion status in `docs/tasks.md` matches actual implementation status
- Progress summaries accurately reflect completion counts
- All completed tasks have corresponding implementation and test evidence

**DOC-002:** Documentation Mismatch between Design and Implementation in feature_generator.py. The `docs/design.md` (Section 4.4) describes `generate_features`'s `feature_config` parameter in a way that implies it's primarily derived from strategy parameters. The actual implementation and other documentation (docs/src/feature_generator.py.md, docs/codebase_overview.md) show a more evolved and flexible feature_config structure that supports three different formats.

**Flaw Impact:** High - Developers referencing docs/design.md for `generate_features` will have an incomplete or misleading understanding of how to configure features, potentially leading to incorrect usage or confusion.

**Root Cause:** The design.md was not updated when the `generate_features` function's feature_config parameter handling was enhanced and finalized during implementation.

**Mandated Solution:** 
1. ✅ **RESOLVED** - Added a prominent note section at the end of docs/design.md that points to docs/src/feature_generator.py.md and docs/codebase_overview.md for the accurate specification
2. ✅ **RESOLVED** - Created a detailed docs/design_errata.md file that explains the discrepancy and documents the three supported feature_config structures accurately
3. ✅ **RESOLVED** - Linked to the errata file from docs/design.md with a clear explanation of the implementation evolution

**Systemic Prevention:** For future projects or major versions, establish a process where design documents are either living documents updated with implementation, or are clearly marked as "initial design" with pointers to detailed implementation docs for evolved components. If a design doc is to remain static, its limitations/deviations from the final implementation must be clearly signposted within the design document itself.

**DOC-004:** Documentation Mismatch (Design vs. Implementation) in `strategies.py`.

**Flaw Impact:** Medium - Developers referencing `docs/design.md` for `strategies.py`'s interface (specifically `generate_sma_crossover_signals` return type) or strategy selection mechanism will have an incomplete or misleading understanding. This could lead to incorrect usage assumptions or confusion when integrating with `main.py`.

**Root Cause:** The `docs/design.md` was not fully updated when the `strategies.py` module was implemented using the Strategy Pattern and when the precise return type of signal generation functions was finalized.

**Mandated Solution:**
1. **REQUIRED** - Update `docs/design.md` (Section 4.5 and/or Section 11) to accurately reflect that `generate_sma_crossover_signals` (and underlying strategy methods) returns a `pd.Series`, not a `pd.DataFrame`.
2. **REQUIRED** - Update `docs/design.md` (Section 4.5 and/or Section 11) to describe the implemented Strategy Pattern (`BaseStrategy`, concrete classes, `STRATEGY_REGISTRY`, `apply_strategy` function) instead of the simpler, direct function call mechanism initially envisioned.
3. **REQUIRED** - Ensure `docs/design_errata.md` clearly details these discrepancies and points to `docs/src/strategies.py.md` as the source of truth for this module.
4. **COMPLETED** - A new entry DOC-004 has been added to `arch_review.md` to track this issue.

**Systemic Prevention:** Similar to DOC-002: For future projects or major versions, establish a process where design documents are either living documents updated with implementation, or are clearly marked as "initial design" with pointers to detailed implementation docs for evolved components. If a design doc is to remain static, its limitations/deviations from the final implementation must be clearly signposted within the design document itself.

---

## RESOLVED CRITICAL FLAWS (This Audit)

**TEST-006 (RESOLVED):** Test Code Quality Degradation in `tests/test_data_loader.py`. The test file contained two nearly identical sets of tests for `fetch` and `fetch_data` functions. ✅ **RESOLVED** - Removed all redundant tests for `fetch` function, kept only a single test to verify delegation to `fetch_data`.

**DOC-001 (RESOLVED):** Documentation Veracity Failure in `docs/tasks.md`. Tasks 20, 21, and 22 were incorrectly marked as incomplete despite full implementation. ✅ **RESOLVED** - Task statuses updated, progress summary corrected, systemic prevention measures mandated.

**DOC-002 (RESOLVED):** Documentation Mismatch in feature_generator.py. The design.md description of `generate_features` didn't match the actual evolved implementation. ✅ **RESOLVED** - Added errata section to design.md and created comprehensive design_errata.md to document the actual supported feature_config structures.

**CODE-001 (RESOLVED):** Code Duplication in `src/backtester.py`. The `PortfolioData` NamedTuple was defined twice, identically, within the file. ✅ **RESOLVED** - Removed the duplicate definition while maintaining all functionality and test coverage.

**API-001 (RESOLVED):** Architectural Degeneration in Test Suite. The test suite for feature generator primarily targeted legacy alias functions (calculate_*) instead of designated primary API functions (add_*). ✅ **RESOLVED** - The tests have been refactored to directly call the primary add_* functions, with separate minimal tests for legacy function delegation.

**INPUT-001 (RESOLVED):** Missing Input Validation in `src/feature_generator.py`. The `add_sma` function lacked validation to ensure the input column is numeric, inconsistent with other similar functions in the same module. ✅ **RESOLVED** - Added explicit numeric type check using `pd.api.types.is_numeric_dtype`, with appropriate error messages and tests.

**TEST-008 (RESOLVED):** Standalone Integration Test Not Integrated into Test Suite. The `integration_test.py` script in the root directory was not integrated into the pytest test suite and used the legacy API. ✅ **RESOLVED** - Refactored into proper pytest test functions in `tests/test_integration.py` that use the recommended `apply_strategy` API.

**DOC-003 (RESOLVED):** Misplaced Documentation File in Incorrect Directory. The `docs/src/test_feature_generator.py.md` file was incorrectly located, as test documentation should be in `docs/tests/`. ✅ **RESOLVED** - Consolidated documentation into `docs/tests/test_feature_generator.py.md` with comprehensive content.

**TEST-009 (RESOLVED):** Test Code Quality Degradation (Duplicate Test File). The file `tests/test_metrics_task25.py` was a complete duplicate of the Task 25 risk/reward metrics tests already present in `tests/test_metrics.py`. ✅ **RESOLVED** - Verified all test functions were duplicated, removed the redundant `tests/test_metrics_task25.py` file, and confirmed that all test coverage is maintained in the main test file.

---

## AUDIT NOTES
- All code and documentation changes related to prior directives have been made and are reflected in the appropriate files.
- Logging standards now specify how logs should be structured to ensure they are testable and observable.
- Test coverage for feature generation is complete.
- Test log capture methods have been corrected.
- Tests for feature generation have been refactored to use static, pre-calculated expected values rather than dynamic recalculation, ensuring independent verification of function correctness.
- Tests for feature generation have been further refactored to directly target the primary API functions (add_*) instead of legacy aliases (calculate_*).
- The design documentation for the `generate_features` function in `feature_generator.py` has been updated to match the implemented behavior. The function uses a `feature_config` dictionary approach rather than the originally designed `strategy_params` approach, providing better separation of concerns and more flexibility in feature generation.
- The discrepancy between design.md and the actual implementation of feature_generator.py has been addressed through a design_errata.md file and a prominent note in design.md, pointing users to accurate documentation while preserving the original design document.
- The data loading interface has been consolidated by enhancing the `fetch_data` function with the additional capabilities from the `fetch` function (column selection and cache control). The `fetch` function is now a backward-compatibility wrapper around `fetch_data`. All relevant documentation has been updated to reflect this change.
- Test imports in `test_backtester.py` have been standardized to use proper Python module imports rather than dynamic imports, improving code clarity and maintainability.
- Test assertions in `test_backtester.py` have been made more precise, ensuring they match the exact expected behavior of the backtesting logic. In particular, portfolio composition tracking assertions now verify exact values (0% cash/100% equity when in position) rather than using less precise comparisons.
- Test code duplication in `test_data_loader.py` has been eliminated by removing redundant tests for the legacy `fetch` function and keeping only one test that verifies the wrapper behavior. This significantly reduced code duplication while maintaining comprehensive test coverage of the primary `fetch_data` function.
- Standalone integration test has been properly integrated into the pytest test suite. The original `integration_test.py` in the project root has been refactored into `tests/test_integration.py` with proper pytest structure and use of the recommended primary API (`apply_strategy`).
- Documentation structure has been standardized by ensuring test documentation resides in `docs/tests/` directory. The misplaced documentation file (`docs/src/test_feature_generator.py.md`) has been consolidated with the correctly located file.

"""Test execution endpoints."""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import subprocess
import json
import os

router = APIRouter()


class TestResult(BaseModel):
    """Individual test result."""
    test_name: str
    status: str  # passed, failed, skipped
    duration: float
    error: Optional[str] = None


class TestRunResult(BaseModel):
    """Complete test run result."""
    timestamp: datetime
    total_tests: int
    passed: int
    failed: int
    skipped: int
    duration: float
    tests: List[TestResult]
    summary: str


class TestStatusResponse(BaseModel):
    """Last test run status."""
    last_run: Optional[datetime]
    status: Optional[str]
    summary: Optional[str]


# Store last test result in memory
_last_test_result: Optional[TestRunResult] = None


@router.get("/test-status", response_model=TestStatusResponse)
async def get_test_status():
    """Get status of last test run."""
    if _last_test_result is None:
        return TestStatusResponse(
            last_run=None,
            status=None,
            summary="Inga tester har körts ännu"
        )

    status = "success" if _last_test_result.failed == 0 else "failed"
    return TestStatusResponse(
        last_run=_last_test_result.timestamp,
        status=status,
        summary=_last_test_result.summary
    )


@router.post("/run-tests", response_model=TestRunResult)
async def run_tests():
    """Run all system tests and return results."""
    global _last_test_result

    timestamp = datetime.utcnow()

    try:
        # Run pytest with JSON report
        result = subprocess.run(
            ["pytest", "tests/", "-v", "--tb=short", "--json-report", "--json-report-file=/tmp/test-report.json"],
            cwd="/Users/gunnar/Code/diff/backend",
            capture_output=True,
            text=True,
            timeout=60
        )

        # Parse JSON report if available
        tests = []
        total_tests = 0
        passed = 0
        failed = 0
        skipped = 0
        duration = 0.0

        try:
            with open("/tmp/test-report.json", "r") as f:
                report = json.load(f)

            duration = report.get("duration", 0.0)

            for test in report.get("tests", []):
                test_name = test.get("nodeid", "unknown")
                status = test.get("outcome", "unknown")
                test_duration = test.get("duration", 0.0)
                error = None

                if status == "failed":
                    call = test.get("call", {})
                    error = call.get("longrepr", "Unknown error")

                tests.append(TestResult(
                    test_name=test_name,
                    status=status,
                    duration=test_duration,
                    error=error
                ))

                total_tests += 1
                if status == "passed":
                    passed += 1
                elif status == "failed":
                    failed += 1
                elif status == "skipped":
                    skipped += 1

        except Exception as e:
            # Fallback: parse stdout
            output_lines = result.stdout.split("\n")
            for line in output_lines:
                if " PASSED" in line or " FAILED" in line or " SKIPPED" in line:
                    total_tests += 1
                    if " PASSED" in line:
                        passed += 1
                    elif " FAILED" in line:
                        failed += 1
                    elif " SKIPPED" in line:
                        skipped += 1

        # Generate summary
        if failed == 0:
            summary = f"✅ Alla {total_tests} tester godkända"
        else:
            summary = f"❌ {failed}/{total_tests} tester misslyckades"

        test_result = TestRunResult(
            timestamp=timestamp,
            total_tests=total_tests,
            passed=passed,
            failed=failed,
            skipped=skipped,
            duration=duration,
            tests=tests,
            summary=summary
        )

        _last_test_result = test_result
        return test_result

    except subprocess.TimeoutExpired:
        test_result = TestRunResult(
            timestamp=timestamp,
            total_tests=0,
            passed=0,
            failed=0,
            skipped=0,
            duration=60.0,
            tests=[],
            summary="❌ Testerna tog för lång tid (timeout)"
        )
        _last_test_result = test_result
        return test_result

    except Exception as e:
        test_result = TestRunResult(
            timestamp=timestamp,
            total_tests=0,
            passed=0,
            failed=0,
            skipped=0,
            duration=0.0,
            tests=[],
            summary=f"❌ Fel vid körning av tester: {str(e)}"
        )
        _last_test_result = test_result
        return test_result

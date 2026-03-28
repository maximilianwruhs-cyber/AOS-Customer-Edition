"""
AOS Customer Edition — Smoke Tests
Validates configuration, packaging, and basic imports.
"""
import os
import json
from pathlib import Path

# Resolve project root (tests/ is one level deep)
PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_config_import():
    """Verify that aos.config imports cleanly without errors."""
    import sys
    sys.path.insert(0, str(PROJECT_ROOT / "src"))
    from aos.config import (
        PROJECT_ROOT as PR,
        DATA_DIR,
        CONFIG_DIR,
        REMOTE_HOSTS_FILE,
        ACTIVE_BACKEND_URL,
    )
    assert PR.exists(), f"PROJECT_ROOT does not exist: {PR}"
    assert CONFIG_DIR.exists(), f"CONFIG_DIR does not exist: {CONFIG_DIR}"
    assert REMOTE_HOSTS_FILE.exists(), f"remote_hosts.json not found"
    assert "localhost" in ACTIVE_BACKEND_URL or "127.0.0.1" in ACTIVE_BACKEND_URL


def test_vsix_exists():
    """Verify the pre-built VS Codium extension is bundled."""
    extensions_dir = PROJECT_ROOT / "deploy" / "extensions"
    vsix_files = list(extensions_dir.glob("*.vsix"))
    assert len(vsix_files) >= 1, "No .vsix extension found in deploy/extensions/"
    for vsix in vsix_files:
        assert vsix.stat().st_size > 1000, f"VSIX file suspiciously small: {vsix}"


def test_remote_hosts_no_internal_ips():
    """Ensure remote_hosts.json contains no internal/private IPs beyond localhost."""
    hosts_file = PROJECT_ROOT / "config" / "remote_hosts.json"
    with open(hosts_file) as f:
        config = json.load(f)
    
    internal_prefixes = ["192.168.", "10.", "172.16.", "172.17.", "172.18."]
    
    for key, host in config.get("hosts", {}).items():
        url = host.get("url", "")
        for prefix in internal_prefixes:
            assert prefix not in url, (
                f"Internal IP found in remote_hosts.json: "
                f"host '{key}' has URL '{url}' containing '{prefix}'"
            )


def test_no_persona_files():
    """Ensure no GZMO persona files leaked into customer edition."""
    persona_files = [
        "core_identity",
        "SOUL.md",
        "HEARTBEAT.md",
        "MEMORY.md",
        "IDENTITY.md",
        "AGENTS.md",
        "USER.md",
    ]
    for name in persona_files:
        path = PROJECT_ROOT / name
        assert not path.exists(), f"Persona file leaked into customer edition: {path}"


def test_rag_engine_import():
    """Verify RAG engine module can be imported (without connecting)."""
    import sys
    sys.path.insert(0, str(PROJECT_ROOT / "src"))
    try:
        from aos.rag_engine import TABLE_NAME, EMBED_DIM, SUPPORTED_EXTENSIONS
        assert TABLE_NAME == "aos_documents"
        assert EMBED_DIM == 768
        assert ".pdf" in SUPPORTED_EXTENSIONS
        assert ".docx" in SUPPORTED_EXTENSIONS
    except ImportError as e:
        # llama_index is an optional dependency (installed via pip install -e '.[rag]')
        if "llama_index" in str(e):
            print(f"    ⚠️  Skipped (optional dep not installed: {e})")
        else:
            raise


def test_project_version():
    """Verify customer edition is v1.0.0."""
    import sys
    sys.path.insert(0, str(PROJECT_ROOT / "src"))
    from aos import __version__
    assert __version__ == "1.0.0", f"Expected v1.0.0, got {__version__}"


def test_pyproject_metadata():
    """Verify pyproject.toml has correct customer edition metadata."""
    import tomllib
    pyproject = PROJECT_ROOT / "pyproject.toml"
    with open(pyproject, "rb") as f:
        data = tomllib.load(f)
    assert data["project"]["name"] == "aos"
    assert data["project"]["version"] == "1.0.0"
    assert "Agentic Operating System" in data["project"]["description"]


if __name__ == "__main__":
    tests = [
        test_config_import,
        test_vsix_exists,
        test_remote_hosts_no_internal_ips,
        test_no_persona_files,
        test_rag_engine_import,
        test_project_version,
        test_pyproject_metadata,
    ]
    
    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            print(f"  ✅ {test.__name__}")
            passed += 1
        except Exception as e:
            print(f"  ❌ {test.__name__}: {e}")
            failed += 1
    
    print(f"\n{'='*40}")
    print(f"  Results: {passed} passed, {failed} failed")
    print(f"{'='*40}")

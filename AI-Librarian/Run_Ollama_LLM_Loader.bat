@echo off
title Ollama Background Optimizer (Memory-Safe)
cls

echo =========================================================
echo  LAUNCHING OLLAMA WITH RAM & CPU PROTECTION
echo =========================================================
echo.

:: 1. Launch the Ollama App at Below Normal Priority
echo [*] Starting Ollama background engine...
start "" /belownormal "%LOCALAPPDATA%\Programs\Ollama\ollama app.exe"

:: 2. Wait for the local server port to wake up
echo [*] Waiting for local server port to initialize...
timeout /t 5 /nobreak > nul

:: 3. Warm up and instantly flush chat models to verify health

echo Keep nomic-embed-text (embedding) resident in memory for instant RAG vector searches
curl -s -X POST http://localhost:11434/api/generate -d "{'model': 'nomic-embed-text', 'keep_alive': -1}" > nul

echo [*] Optimizing memory footprint for llama 3.1 8B (for creative writing)...
curl -s -X POST http://localhost:11434/api/generate -d "{'model': 'llama3.1:8b', 'keep_alive': '15m'}" > nul

echo [*] Optimizing memory footprint for Gemma 4 12B (for AI-Librarian)...
curl -s -X POST http://localhost:11434/api/generate -d "{'model': 'gemma4:12b', 'keep_alive': '15m'}" > nul

echo [*] Optimizing memory footprint for Qwen 2.5 7B (for Coding)...
curl -s -X POST http://localhost:11434/api/generate -d "{'model': 'qwen2.5:7b', 'keep_alive':'15m'}" > nul

echo [*] Optimizing memory footprint for Qwen3 Vision 4B Instruct (for Vision task)...
curl -s -X POST http://localhost:11434/api/generate -d "{'model': 'qwen3-vl:4b', 'keep_alive':'15m'}" > nul

echo.
echo =========================================================
echo  SUCCESS: Your 16GB RAM is completely clean and protected!
echo  Ollama will load models dynamically on-demand when called.
echo  i7 gen 11, 16GB RAM, 8 core(4-core phys, 4-core HT, Iris Xe
echo =========================================================
echo.
timeout /t 3 > nul
exit




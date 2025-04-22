import argparse
import asyncio

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--transport", choices=["stdio", "sse"], default="stdio")
    args = parser.parse_args()

    if args.transport == "stdio":
        from stdio_transport import run_stdio
        asyncio.run(run_stdio())
    else:
        from sse_transport import run_sse
        run_sse()

if __name__ == "__main__":
    main()
# test_model.py
import aiohttp
import asyncio
import json
import time
from datetime import datetime
from statistics import mean, median, stdev
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.panel import Panel
from concurrent.futures import ThreadPoolExecutor

console = Console()


class Benchmark:
    def __init__(self, num_requests=10, concurrency=5):
        self.num_requests = num_requests
        self.concurrency = concurrency
        self.url = "http://localhost:8000/v1/completions"
        self.results = []
        self.errors = []

    async def make_request(self, session, request_id):
        data = {
            "model": "/models/Lumo-8B-Instruct-FT-Q4_0.gguf",
            "prompt": "What is artificial intelligence?",
            "max_tokens": 100,
            "temperature": 0.7,
        }

        start_time = time.time()
        try:
            async with session.post(self.url, json=data) as response:
                await response.json()
                duration = time.time() - start_time
                self.results.append(duration)
                return duration, None
        except Exception as e:
            duration = time.time() - start_time
            error_msg = f"Request {request_id} failed: {str(e)}"
            self.errors.append(error_msg)
            return duration, error_msg

    async def run_benchmark(self):
        async with aiohttp.ClientSession() as session:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                TimeElapsedColumn(),
                console=console,
            ) as progress:
                task = progress.add_task(
                    "[cyan]Running benchmark...", total=self.num_requests
                )

                # Create pool of requests
                tasks = []
                for i in range(self.num_requests):
                    tasks.append(self.make_request(session, i))

                    # Control concurrency
                    if len(tasks) >= self.concurrency:
                        results = await asyncio.gather(*tasks)
                        tasks = []
                        progress.update(task, advance=self.concurrency)

                # Handle remaining tasks
                if tasks:
                    results = await asyncio.gather(*tasks)
                    progress.update(task, advance=len(tasks))

    def generate_report(self):
        if not self.results:
            console.print("[red]No results to report!")
            return

        # Calculate statistics
        total_time = sum(self.results)
        avg_time = mean(self.results)
        med_time = median(self.results)
        try:
            std_dev = stdev(self.results)
        except:
            std_dev = 0

        requests_per_second = self.num_requests / total_time
        success_rate = (
            (self.num_requests - len(self.errors)) / self.num_requests
        ) * 100

        # Create rich table
        table = Table(
            title="Benchmark Results", show_header=True, header_style="bold magenta"
        )
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Total Requests", str(self.num_requests))
        table.add_row("Concurrency Level", str(self.concurrency))
        table.add_row("Total Time", f"{total_time:.2f} seconds")
        table.add_row("Requests/second", f"{requests_per_second:.2f}")
        table.add_row("Mean Response Time", f"{avg_time * 1000:.2f} ms")
        table.add_row("Median Response Time", f"{med_time * 1000:.2f} ms")
        table.add_row("Std Dev", f"{std_dev * 1000:.2f} ms")
        table.add_row("Success Rate", f"{success_rate:.1f}%")

        # Print report
        console.print("\n")
        console.print(
            Panel.fit(
                "[bold green]Benchmark Complete![/bold green]",
                subtitle=f"[blue]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/blue]",
            )
        )
        console.print("\n")
        console.print(table)

        # Print errors if any
        if self.errors:
            console.print("\n[red]Errors encountered:[/red]")
            for error in self.errors:
                console.print(f"[red]• {error}[/red]")


async def main():
    # You can adjust these parameters
    num_requests = 100
    concurrency = 10

    benchmark = Benchmark(num_requests=num_requests, concurrency=concurrency)

    console.print(
        Panel.fit(
            "[bold yellow]Starting Benchmark[/bold yellow]",
            subtitle="[blue]vLLM Performance Test[/blue]",
        )
    )

    await benchmark.run_benchmark()
    benchmark.generate_report()


if __name__ == "__main__":
    # Install required packages:
    # pip install aiohttp rich
    asyncio.run(main())

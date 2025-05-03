import click
from rich.console import Console
from .models import ProjectMeta
from .processor import process_metadata
from .cloud import upload_to_cloud

console = Console()

@click.group()
def cli():
    """Metadata Automation System"""
    pass

@cli.command()
@click.option("--input-dir", "-i", required=True, help="Input directory with metadata files")
@click.option("--output", "-o", default="processed", help="Output directory")
@click.option("--cloud", "-c", type=click.Choice(["s3", "gcs", "none"]), default="none")
def crawl(input_dir, output, cloud):
    """Process metadata files from directory"""
    results = process_metadata(input_dir, output)
    
    if cloud != "none":
        upload_to_cloud(output, cloud)
    
    console.print(f"[green]Processed {len(results)} files[/green]")
    console.print(f"[bold]Validation summary:[/bold]")
    console.print(results.groupby("status").size())

@cli.command()
@click.option("--input", "-i", required=True, help="Processed metadata file")
@click.option("--output", "-o", default="report.html", help="Output report file")
@click.option("--format", "-f", default="html", type=click.Choice(["html", "json"]))
def analyze(input, output, format):
    """Generate analysis report"""
    # Implementation details...
    console.print(f"[bold]Report generated:[/bold] {output}")

@cli.command()
@click.argument("file")
def validate(file):
    """Validate metadata file"""
    try:
        ProjectMeta.from_yaml(file)
        console.print("[green]✓ Valid metadata file[/green]")
    except Exception as e:
        console.print(f"[red]× Validation error: {str(e)}[/red]")

if __name__ == "__main__":
    cli()

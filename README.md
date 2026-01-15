Auto File Type Organizer is a Python utility that automatically scans a specified directory, detects all file types dynamically (without hard-coding extensions), and organizes files into structured folders based on their file extension.

The script generates and maintains a fileTypes.txt registry containing all detected file types, then uses this registry to ensure corresponding folders exist (e.g., Files Type jpg, Files Type pdf). Files are safely moved into their respective folders while directories and critical control files are explicitly excluded from processing.

The tool is idempotent and safe to run multiple times — it will not duplicate files, recreate existing folders unnecessarily, or move its own configuration file.

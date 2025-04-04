# GPS Telemetry Processing Pipeline

A serverless pipeline for processing high-volume GPS telemetry data from delivery vehicles.

## Project Structure

```
backend/L2/
├── scripts/           # Utility scripts for deployment and data management
├── lambdas/          # Lambda function code
├── utils/            # Shared utilities
├── data/            # Generated test data
├── .env             # Environment variables (not in git)
├── .env.example     # Example environment variables
├── README.md        # This file
├── ARCHITECTURE.md  # System architecture documentation
└── TRADEOFFS.md     # Design trade-offs documentation
```

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and fill in your AWS credentials:
   ```bash
   cp .env.example .env
   ```

## Usage

### Deploy Lambda Functions

```bash
python scripts/deploy_lambda.py
```

### Generate and Upload Test Data

```bash
python scripts/main.py
```

## Architecture

The system uses the following AWS services:
- S3 for data storage
- Lambda for serverless processing
- SQS for message queuing
- DynamoDB for data persistence
- Redis for metadata caching

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed design documentation.

## Development

- Branch naming: `feature/description` for features, `fix/description` for fixes
- Commit messages follow conventional commits format
- PRs should include tests and documentation updates

## Testing

```bash
python -m pytest tests/
```

## License

MIT 
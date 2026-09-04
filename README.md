# QuickSight MCP Server

A Model Context Protocol (MCP) server for Amazon QuickSight that enables AI assistants to create and manage QuickSight dashboards, analyses, datasets, and data sources.

## Features

### 🔍 Discovery Tools (23 Read Operations)
- `quicksight_overview` - Get account-wide QuickSight statistics
- `list_*` - List datasets, data sources, analyses, dashboards, templates, themes, refresh schedules, dashboard versions
- `describe_*` - Get detailed information about any resource, including full analysis/dashboard/template definitions
- `search_*` - Search datasets, data sources, analyses, and dashboards by filter

### 📝 Write Operations (29 Tools)

**Data Sources** (4 tools)
- Create, update, and delete data sources (RDS, Redshift, S3, Athena, etc.)
- Manage data source permissions

**Datasets** (4 tools)
- Create datasets with physical/logical tables
- Update schemas and transformations, delete datasets
- Manage dataset permissions

**Analyses** (5 tools)
- Build analyses with visuals, filters, parameters
- Update analysis definitions
- Delete and restore analyses
- Control analysis access

**Dashboards** (5 tools)
- Create dashboards from analyses
- Update and publish dashboard versions, delete dashboards
- Manage viewer/editor permissions

**Data Ingestion** (5 tools)
- Trigger and cancel SPICE data refresh
- Create, update, and delete refresh schedules

**Templates** (3 tools)
- Create, update, and delete templates

**Themes** (3 tools)
- Create, update, and delete themes

### 🔗 Embedding (4 Tools)
- Generate embed URLs for registered and anonymous users
- Dashboard and console session embed URLs

**Total: 56 tools for complete QuickSight management**

## Installation

### Prerequisites

- macOS or Linux
- [uv](https://docs.astral.sh/uv/) — it installs and pins the right Python for you
- An AWS account with QuickSight activated in the target region, and credentials carrying the permissions listed under [Required AWS Permissions](#required-aws-permissions)

```bash
xcode-select --install                            # git + toolchain (macOS)
curl -LsSf https://astral.sh/uv/install.sh | sh   # uv; restart your shell afterwards
```

Python is not a separate step: `.python-version` pins 3.13 and `uv` fetches it automatically.

### Setup

1. **Clone and install dependencies**:

```bash
git clone git@github.com:xenolab007/anhminhnguyen3110-quicksight-mcp.git
cd anhminhnguyen3110-quicksight-mcp
uv sync
```

`uv sync` creates `.venv` and installs the locked dependency set from `uv.lock`. Add `--extra server` only if you need the SSE or HTTP transports; the stdio transport that MCP clients use does not require it.

2. **Configure credentials**:

`.env` is gitignored, so it does not arrive with the clone and must be created on every machine:

```bash
cp .env.example .env
chmod 600 .env
```

Required `.env` variables:

```bash
AWS_ACCOUNT_ID=123456789012
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
```

Leave the two key variables out to fall back to the default boto3 credential chain instead (`~/.aws/credentials`, `AWS_PROFILE`, SSO, instance roles). `MCP_HOST` and `MCP_PORT` are optional and affect only the SSE/HTTP transports.

> **`.env` is read from the current working directory**, not from the repo directory. Start the server with the repo as its working directory, or supply configuration through `--aws-account-id` / `--aws-region` flags or real environment variables.

> The `.env` parser is deliberately minimal: no quotes, no inline comments, no `export` prefix. `KEY="value"` keeps the quotes as part of the value, and a real environment variable of the same name always wins over `.env`.

3. **Verify the install**:

```bash
uv run main.py     # expect "All tools registered successfully"; Ctrl-C to exit
```

## Usage

### STDIO Transport (for MCP clients)

```bash
uv run main.py
```

**Claude Code** — register once and use it from any project:

```bash
claude mcp add quicksight -s user -- sh -c 'cd /path/to/anhminhnguyen3110-quicksight-mcp && exec .venv/bin/python main.py'
```

The `cd` is required so that `.env` resolves; without it the server exits with `Configuration error: AWS_ACCOUNT_ID is required`. Use `-s local` to scope the server to a single project, or `-s project` to commit it to `.mcp.json` for the team.

**Claude Desktop** — add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "quicksight": {
      "command": "sh",
      "args": [
        "-c",
        "cd /path/to/anhminhnguyen3110-quicksight-mcp && exec .venv/bin/python main.py"
      ]
    }
  }
}
```

### SSE Transport (for web clients)

```bash
uv run main.py --transport sse --host 0.0.0.0 --port 8080
```

### HTTP Transport (RESTful API)

```bash
uv run main.py --transport http --port 3000
```

### Debug Mode

```bash
uv run main.py --debug
```

## Available Tools

### Discovery Tools

| Tool | Description |
|------|-------------|
| `quicksight_overview` | Get overview statistics of all resources |
| `list_dashboards` | List all dashboards with IDs and names |
| `list_analyses` | List all analyses with IDs and names |
| `list_datasets` | List all datasets with IDs and names |
| `list_datasources` | List all data sources with IDs and names |
| `describe_dashboard` | Get detailed dashboard information |
| `describe_analysis` | Get detailed analysis definition |
| `describe_dataset` | Get dataset schema and configuration |
| `describe_datasource` | Get data source connection details |

### Example Prompts for Claude

```
"Show me all my QuickSight dashboards"

"What datasets are available in my account?"

"Describe the schema of dataset xyz-123"

"Give me an overview of my QuickSight resources"
```

## Project Structure

```
quicksight-mcp/
├── main.py                          # Entry point with CLI
├── pyproject.toml                   # Project configuration
├── .env.example                     # Environment template
│
├── quicksight_mcp/                  # Main package
│   ├── __init__.py
│   ├── config.py                    # Configuration management
│   ├── server.py                    # MCP server setup
│   ├── service.py                   # QuickSight API wrapper
│   │
│   ├── tools/                       # MCP tools
│   │   ├── __init__.py
│   │   ├── discovery.py            # Read operations
│   │   ├── datasource.py           # Data source tools (coming)
│   │   ├── dataset.py              # Dataset tools (coming)
│   │   ├── analysis.py             # Analysis tools (coming)
│   │   └── dashboard.py            # Dashboard tools (coming)
│   │
│   └── models/                      # Data models
│       └── __init__.py
```

## Development

### Adding New Tools

1. Create a new file in `quicksight_mcp/tools/`
2. Define your tool functions
3. Register them in the tool module
4. Import and register in `main.py`

Example:
```python
# quicksight_mcp/tools/my_tools.py
def register_my_tools(mcp):
    @mcp.tool(name="my_tool")
    async def my_tool(param: str) -> dict:
        config = mcp.config
        service = QuickSightService(config.aws_account_id, config.aws_region)
        # Your logic here
        return {}
```

## Architecture

### Multi-Transport Support
- **STDIO**: For Claude Desktop integration
- **SSE**: For streaming web clients
- **HTTP**: For RESTful API access

### Configuration Management
- Environment variables from `.env` file
- CLI argument overrides
- AWS credentials support

### QuickSight Service Layer
- Clean boto3 wrapper
- Error handling and logging
- Pagination support for large results

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is open source and available under the MIT License.

## Roadmap

- [x] Basic read operations
- [x] Multi-transport support  
- [x] Environment configuration
- [ ] Data source write operations
- [ ] Dataset creation and updates
- [ ] Analysis generation
- [ ] Dashboard publishing
- [ ] Permission management
- [ ] Template support
- [ ] Theme management

## Support

For questions or issues, please open an issue on GitHub.

#### `quicksight_overview`
Provides a comprehensive overview of QuickSight resources in the account.
```
Parameters:
- account_id (required): AWS account ID
- region (optional): AWS region (default: us-east-1)
```

## Usage Examples

### Basic Resource Listing
```bash
# List all dashboards
q chat "List all QuickSight dashboards in account 123456789012"

# List analyses in a specific region
q chat "Show me all analyses in us-west-2 for account 123456789012"
```
### Account Overview
```bash
# Get comprehensive QuickSight statistics
q chat "Give me an overview of QuickSight resources in account 123456789012"
```

## Required AWS Permissions

Read-only tools (`list_*`, `describe_*`, `search_*`, `quicksight_overview`) need:

- `quicksight:List*`, `quicksight:Describe*`, `quicksight:Search*`

Write tools need the matching action per resource, for example:

- Analyses — `CreateAnalysis`, `UpdateAnalysis`, `DeleteAnalysis`, `RestoreAnalysis`
- Dashboards — `CreateDashboard`, `UpdateDashboard`, `UpdateDashboardPublishedVersion`, `DeleteDashboard`
- Datasets / data sources — `CreateDataSet`, `UpdateDataSet`, `DeleteDataSet`, `CreateDataSource`, `UpdateDataSource`, `DeleteDataSource`
- Ingestion — `CreateIngestion`, `CancelIngestion`, `CreateRefreshSchedule`, `UpdateRefreshSchedule`, `DeleteRefreshSchedule`
- Templates / themes — `CreateTemplate`, `UpdateTemplate`, `DeleteTemplate`, `CreateTheme`, `UpdateTheme`, `DeleteTheme`
- Permission tools — `UpdateAnalysisPermissions`, `UpdateDashboardPermissions`, `UpdateDataSetPermissions`, `UpdateDataSourcePermissions`
- Embedding — `GenerateEmbedUrlForRegisteredUser`, `GenerateEmbedUrlForAnonymousUser`

Grant only what the deployment actually needs. The `delete_*` tools are destructive and are worth withholding from read-only or exploratory setups.

## Common Use Cases

### Data Governance
- Identify impact of data source changes
- Audit data dependencies across your organization

### Resource Management
- Inventory all QuickSight resources
- Identify unused or orphaned resources
- Plan resource migrations or cleanup

### Troubleshooting
- Diagnose dashboard or analysis issues by examining dependencies
- Understand data flow when reports show unexpected results
- Validate data source configurations

## Error Handling

The server provides detailed error messages for common issues:
- Invalid account IDs or resource IDs
- Insufficient permissions
- Resources not found
- Region-specific access issues

## Support

For issues or questions about this MCP server, please refer to the MCP documentation or contact your system administrator.


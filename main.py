"""QuickSight MCP Server - Entry point with multi-transport support"""

import argparse
import logging
import sys
from quicksight_mcp.config import Config
from quicksight_mcp.server import create_server
from quicksight_mcp.tools import (
    discovery, datasource, dataset, analysis, dashboard, ingestion,
    embed, search, template, theme
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point for QuickSight MCP Server"""
    parser = argparse.ArgumentParser(
        description='QuickSight MCP Server for AI Dashboard Generation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with STDIO transport (default - for Claude Desktop)
  python main.py
  
  # Run with SSE transport
  python main.py --transport sse --host 0.0.0.0 --port 8080
  
  # Run with HTTP transport
  python main.py --transport http --port 3000

Configuration is loaded from .env file or environment variables.
Required: AWS_ACCOUNT_ID
        """
    )
    
    parser.add_argument(
        '--transport',
        choices=['stdio', 'sse', 'http'],
        default='stdio',
        help='Transport protocol (default: stdio)'
    )
    parser.add_argument(
        '--host',
        default=None,
        help='Host for SSE/HTTP server (default: from .env or 127.0.0.1)'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=None,
        help='Port for SSE/HTTP server (default: from .env or 8000)'
    )
    
    # AWS Configuration
    parser.add_argument(
        '--aws-account-id',
        default=None,
        help='AWS Account ID (overrides .env)'
    )
    parser.add_argument(
        '--aws-region',
        default=None,
        help='AWS Region (overrides .env, default: us-east-1)'
    )
    parser.add_argument(
        '--aws-access-key-id',
        default=None,
        help='AWS Access Key ID (overrides .env)'
    )
    parser.add_argument(
        '--aws-secret-access-key',
        default=None,
        help='AWS Secret Access Key (overrides .env)'
    )
    parser.add_argument(
        '--aws-session-token',
        default=None,
        help='AWS Session Token for temporary credentials (overrides .env)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")
    
    try:
        # Load configuration from .env file with CLI overrides
        config = Config.from_env(
            aws_account_id=args.aws_account_id,
            aws_region=args.aws_region,
            aws_access_key_id=args.aws_access_key_id,
            aws_secret_access_key=args.aws_secret_access_key,
            aws_session_token=args.aws_session_token
        )
        
        # Override with CLI arguments if provided
        if args.host:
            config.mcp_host = args.host
        if args.port:
            config.mcp_port = args.port
        
        logger.info("Starting QuickSight MCP Server...")
        logger.info(f"AWS Account: {config.aws_account_id}")
        logger.info(f"AWS Region: {config.aws_region}")
        logger.info(f"Transport: {args.transport}")
        
        # Create MCP server
        mcp = create_server(config)
        
        # Register all tools
        logger.info("Registering discovery tools...")
        discovery.register_discovery_tools(mcp)
        
        logger.info("Registering data source tools...")
        datasource.register_datasource_tools(mcp)
        
        logger.info("Registering dataset tools...")
        dataset.register_dataset_tools(mcp)
        
        logger.info("Registering analysis tools...")
        analysis.register_analysis_tools(mcp)
        
        logger.info("Registering dashboard tools...")
        dashboard.register_dashboard_tools(mcp)
        
        logger.info("Registering ingestion tools...")
        ingestion.register_ingestion_tools(mcp)
        
        logger.info("Registering embed URL tools...")
        embed.register_embed_tools(mcp)
        
        logger.info("Registering search tools...")
        search.register_search_tools(mcp)
        
        logger.info("Registering template tools...")
        template.register_template_tools(mcp)
        
        logger.info("Registering theme tools...")
        theme.register_theme_tools(mcp)
        
        logger.info("All tools registered successfully")
        
        # Run server with selected transport
        if args.transport == 'stdio':
            logger.info("Running with STDIO transport...")
            mcp.run(transport='stdio')
            
        elif args.transport == 'sse':
            logger.info(f"Running with SSE transport on {config.mcp_host}:{config.mcp_port}...")
            mcp.settings.host = config.mcp_host
            mcp.settings.port = config.mcp_port
            mcp.run(transport='sse')

        elif args.transport == 'http':
            logger.info(f"Running with HTTP transport on {config.mcp_host}:{config.mcp_port}...")
            mcp.settings.host = config.mcp_host
            mcp.settings.port = config.mcp_port
            mcp.run(transport='streamable-http')
        
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        logger.error("Make sure .env file exists with AWS_ACCOUNT_ID set.")
        sys.exit(1)
        
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

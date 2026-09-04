"""Template management tools for QuickSight"""

import logging
from quicksight_mcp.services.template import TemplateService
from quicksight_mcp.models.tool_models import (
    ListTemplatesRequest, ListTemplatesResponse,
    DescribeTemplateRequest, DescribeTemplateResponse,
    DescribeTemplateDefinitionRequest, DescribeTemplateDefinitionResponse,
    CreateTemplateRequest, CreateTemplateResponse,
    UpdateTemplateRequest, UpdateTemplateResponse,
    PaginationInfo, ErrorInfo,
    DeleteTemplateRequest, DeleteTemplateResponse,
)
from quicksight_mcp.models.template import (
    CreateTemplateRequest as TemplateCreateRequest,
    UpdateTemplateRequest as TemplateUpdateRequest,
    TemplateSourceEntity
)

logger = logging.getLogger(__name__)


def register_template_tools(mcp):
    """Register all template management tools with the MCP server"""
    
    @mcp.tool(
        name="list_templates",
        description="List all templates in the QuickSight account"
    )
    async def list_templates(request: ListTemplatesRequest) -> ListTemplatesResponse:
        """List all templates with their IDs and names"""
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = TemplateService(quicksight, config.aws_account_id)
            all_templates = service.list_templates()
            
            # Apply pagination
            limit = 10
            start_idx = request.offset
            end_idx = start_idx + limit
            paginated = all_templates[start_idx:end_idx]
            
            # Format templates
            formatted_templates = [
                {'TemplateId': t['TemplateId'], 'Name': t.get('Name', t['TemplateId'])}
                for t in paginated
            ]
            
            return ListTemplatesResponse(
                templates=formatted_templates,
                pagination=PaginationInfo(
                    limit=10,
                    offset=request.offset,
                    total=len(all_templates),
                    has_more=end_idx < len(all_templates),
                    next_offset=end_idx if end_idx < len(all_templates) else None
                ),
                status="SUCCESS"
            )
        except Exception as e:
            logger.error(f"Error listing templates: {str(e)}")
            return ListTemplatesResponse(
                templates=[],
                pagination=PaginationInfo(limit=10, offset=request.offset, total=0, has_more=False),
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="describe_template",
        description="Get detailed information about a specific template"
    )
    async def describe_template(request: DescribeTemplateRequest) -> DescribeTemplateResponse:
        """
        Get template details
        
        Args:
            request: Request with template_id, version_number, and alias_name
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = TemplateService(quicksight, config.aws_account_id)
            template = service.describe_template(
                request.template_id,
                request.version_number,
                request.alias_name
            )
            return DescribeTemplateResponse(
                template=template,
                status="SUCCESS"
            )
        except Exception as e:
            logger.error(f"Error describing template {request.template_id}: {str(e)}")
            return DescribeTemplateResponse(
                template={},
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="describe_template_definition",
        description="Get the definition (structure) of a template"
    )
    async def describe_template_definition(request: DescribeTemplateDefinitionRequest) -> DescribeTemplateDefinitionResponse:
        """
        Get template definition with full structure
        
        Args:
            request: Request with template_id, version_number, and alias_name
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = TemplateService(quicksight, config.aws_account_id)
            response = service.describe_template_definition(
                template_id=request.template_id,
                version_number=request.version_number,
                alias_name=request.alias_name
            )
            
            logger.info(f"Retrieved template definition for {request.template_id}")
            
            return DescribeTemplateDefinitionResponse(
                template_id=response.get('TemplateId', request.template_id),
                definition=response.get('Definition', {}),
                errors=response.get('Errors', []),
                status="SUCCESS"
            )
            
        except Exception as e:
            logger.error(f"Error describing template definition: {str(e)}")
            return DescribeTemplateDefinitionResponse(
                template_id=request.template_id,
                definition={},
                errors=[],
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="create_template",
        description="Create a new QuickSight template"
    )
    async def create_template(request: CreateTemplateRequest) -> CreateTemplateResponse:
        """
        Create a new template from analysis or existing template
        
        Args:
            request: CreateTemplateRequest with all template configuration
            
        Returns:
            CreateTemplateResponse with creation status and template ARN
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = TemplateService(quicksight, config.aws_account_id)
            
            # Convert source_entity dict to model if provided
            source_entity_model = None
            if request.source_entity:
                source_entity_model = TemplateSourceEntity(
                    source_analysis=request.source_entity.get('SourceAnalysis'),
                    source_template=request.source_entity.get('SourceTemplate')
                )
            
            template_request = TemplateCreateRequest(
                template_id=request.template_id,
                name=request.name,
                source_entity=source_entity_model,
                definition=None,
                permissions=request.permissions,
                version_description=request.version_description,
                tags=request.tags
            )
            
            response = service.create_template(template_request)
            
            logger.info(f"Created template: {request.template_id}")
            
            return CreateTemplateResponse(
                arn=response.get('Arn', ''),
                template_id=response.get('TemplateId', request.template_id),
                version_arn=response.get('VersionArn', ''),
                creation_status=response.get('CreationStatus', 'CREATION_IN_PROGRESS'),
                status="SUCCESS"
            )
            
        except Exception as e:
            logger.error(f"Error creating template {request.template_id}: {str(e)}")
            return CreateTemplateResponse(
                arn="",
                template_id=request.template_id,
                version_arn="",
                creation_status="FAILED",
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="update_template",
        description="Update an existing QuickSight template"
    )
    async def update_template(request: UpdateTemplateRequest) -> UpdateTemplateResponse:
        """
        Update an existing template (creates new version)
        
        Args:
            request: UpdateTemplateRequest with updated configuration
            
        Returns:
            UpdateTemplateResponse with update status and version number
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = TemplateService(quicksight, config.aws_account_id)
            
            # Convert source_entity dict to model if provided
            source_entity_model = None
            if request.source_entity:
                source_entity_model = TemplateSourceEntity(
                    source_analysis=request.source_entity.get('SourceAnalysis'),
                    source_template=request.source_entity.get('SourceTemplate')
                )
            
            template_request = TemplateUpdateRequest(
                template_id=request.template_id,
                source_entity=source_entity_model,
                definition=None,
                name=request.name,
                version_description=request.version_description
            )
            
            response = service.update_template(template_request)
            
            logger.info(f"Updated template: {request.template_id}")
            
            return UpdateTemplateResponse(
                arn=response.get('Arn', ''),
                template_id=response.get('TemplateId', request.template_id),
                version_arn=response.get('VersionArn', ''),
                update_status=response.get('UpdateStatus', 'UPDATE_IN_PROGRESS'),
                status="SUCCESS"
            )
            
        except Exception as e:
            logger.error(f"Error updating template {request.template_id}: {str(e)}")
            return UpdateTemplateResponse(
                arn="",
                template_id=request.template_id,
                version_arn="",
                update_status="FAILED",
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="delete_template",
        description=(
            "Permanently delete a template. Pass version_number to delete only that one "
            "version instead of the whole template. This cannot be undone."
        )
    )
    async def delete_template(request: DeleteTemplateRequest) -> DeleteTemplateResponse:
        """Delete a template or one of its versions"""
        config = mcp.config
        quicksight = mcp.quicksight

        try:
            service = TemplateService(quicksight, config.aws_account_id)
            response = service.delete_template(
                template_id=request.template_id,
                version_number=request.version_number
            )

            return DeleteTemplateResponse(
                template_id=response.get('TemplateId', request.template_id),
                arn=response.get('Arn', ''),
                status="SUCCESS"
            )

        except Exception as e:
            logger.error(f"Error deleting template: {str(e)}")
            return DeleteTemplateResponse(
                template_id=request.template_id,
                arn="",
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )

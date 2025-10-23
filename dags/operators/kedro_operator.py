"""
Custom Kedro Operator for Apache Airflow.

This operator allows running Kedro pipelines and nodes from Airflow DAGs.
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from airflow.models import BaseOperator
# apply_defaults is deprecated in newer Airflow versions
from kedro.framework.project import configure_project
from kedro.framework.session import KedroSession

logger = logging.getLogger(__name__)


class KedroOperator(BaseOperator):
    """
    Airflow operator to run Kedro pipelines and nodes.
    
    This operator creates a Kedro session and executes specified nodes
    from a Kedro pipeline, integrating Kedro's ML workflows with Airflow's
    orchestration capabilities.
    
    Args:
        package_name: Name of the Kedro package (e.g., 'spaceflights')
        pipeline_name: Name of the pipeline to run (e.g., 'data_processing')
        node_name: Name(s) of the node(s) to execute
        project_path: Path to the Kedro project root
        env: Kedro environment to use (e.g., 'local', 'production')
        conf_source: Path to configuration files
        
    Example:
        >>> task = KedroOperator(
        ...     task_id="preprocess_data",
        ...     package_name="spaceflights",
        ...     pipeline_name="data_processing",
        ...     node_name="preprocess_companies_node",
        ...     project_path="/app",
        ...     env="local",
        ... )
    """

    ui_color = "#ffc900"  # Kedro yellow
    ui_fgcolor = "#000000"

    def __init__(
        self,
        package_name: str,
        pipeline_name: str,
        node_name: str | list[str],
        project_path: str | Path,
        env: str = "local",
        conf_source: str = "",
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.package_name = package_name
        self.pipeline_name = pipeline_name
        self.node_name = node_name if isinstance(node_name, list) else [node_name]
        self.project_path = Path(project_path)
        self.env = env
        self.conf_source = conf_source or str(self.project_path / "conf")

    def execute(self, context: Any) -> None:
        """
        Execute the Kedro node(s) within an Airflow task.
        
        This method:
        1. Configures the Kedro project
        2. Creates a Kedro session
        3. Runs the specified nodes
        4. Logs execution details
        
        Args:
            context: Airflow task context
        """
        logger.info(f"Executing Kedro operator for package: {self.package_name}")
        logger.info(f"Pipeline: {self.pipeline_name}")
        logger.info(f"Nodes: {self.node_name}")
        logger.info(f"Environment: {self.env}")
        
        try:
            # Configure Kedro project
            configure_project(self.package_name)
            logger.info("Kedro project configured successfully")
            
            # Create and run Kedro session
            with KedroSession.create(
                project_path=self.project_path,
                env=self.env,
                conf_source=self.conf_source,
            ) as session:
                logger.info("Kedro session created")
                
                # Run the pipeline with specified nodes
                session.run(
                    pipeline_name=self.pipeline_name,
                    node_names=self.node_name,
                )
                
                logger.info("Pipeline execution completed successfully")
                
        except Exception as e:
            logger.error(f"Error executing Kedro pipeline: {str(e)}")
            raise


"""
Functional tests for Airflow DAGs
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add dags directory to path
dags_dir = Path(__file__).parent.parent.parent / "dags"
sys.path.insert(0, str(dags_dir))


class TestAirflowDAGs:
    """Test Airflow DAGs functionality"""
    
    def test_dag_imports(self):
        """Test that all DAGs can be imported without errors"""
        try:
            import spaceflights_advanced_ml_pipeline
            import spaceflights_daily_data_processing
            import spaceflights_ml_pipeline
            import spaceflights_on_demand
            import spaceflights_weekly_model_training
            assert True
        except ImportError as e:
            pytest.fail(f"DAG import failed: {e}")
    
    def test_advanced_ml_dag_structure(self):
        """Test Advanced ML DAG structure"""
        try:
            import spaceflights_advanced_ml_pipeline
            
            # Check if DAG is defined
            assert hasattr(spaceflights_advanced_ml_pipeline, 'dag')
            dag = spaceflights_advanced_ml_pipeline.dag
            
            # Check DAG properties
            assert dag.dag_id == "spaceflights_advanced_ml_pipeline"
            assert dag.description is not None
            assert dag.schedule is not None
            
            # Check that DAG has tasks
            assert len(dag.tasks) > 0
            
        except Exception as e:
            pytest.fail(f"Advanced ML DAG structure test failed: {e}")
    
    def test_daily_processing_dag_structure(self):
        """Test Daily Data Processing DAG structure"""
        try:
            import spaceflights_daily_data_processing
            
            # Check if DAG is defined
            assert hasattr(spaceflights_daily_data_processing, 'dag')
            dag = spaceflights_daily_data_processing.dag
            
            # Check DAG properties
            assert dag.dag_id == "spaceflights_daily_data_processing"
            assert dag.description is not None
            assert dag.schedule is not None
            
            # Check that DAG has tasks
            assert len(dag.tasks) > 0
            
        except Exception as e:
            pytest.fail(f"Daily processing DAG structure test failed: {e}")
    
    def test_ml_pipeline_dag_structure(self):
        """Test ML Pipeline DAG structure"""
        try:
            import spaceflights_ml_pipeline
            
            # Check if DAG is defined
            assert hasattr(spaceflights_ml_pipeline, 'dag')
            dag = spaceflights_ml_pipeline.dag
            
            # Check DAG properties
            assert dag.dag_id == "spaceflights_ml_pipeline"
            assert dag.description is not None
            assert dag.schedule is not None
            
            # Check that DAG has tasks
            assert len(dag.tasks) > 0
            
        except Exception as e:
            pytest.fail(f"ML pipeline DAG structure test failed: {e}")
    
    def test_on_demand_dag_structure(self):
        """Test On-Demand DAG structure"""
        try:
            import spaceflights_on_demand
            
            # Check if DAG is defined
            assert hasattr(spaceflights_on_demand, 'dag')
            dag = spaceflights_on_demand.dag
            
            # Check DAG properties
            assert dag.dag_id == "spaceflights_on_demand"
            assert dag.description is not None
            assert dag.schedule is None  # Manual trigger only
            
            # Check that DAG has tasks
            assert len(dag.tasks) > 0
            
        except Exception as e:
            pytest.fail(f"On-demand DAG structure test failed: {e}")
    
    def test_weekly_training_dag_structure(self):
        """Test Weekly Model Training DAG structure"""
        try:
            import spaceflights_weekly_model_training
            
            # Check if DAG is defined
            assert hasattr(spaceflights_weekly_model_training, 'dag')
            dag = spaceflights_weekly_model_training.dag
            
            # Check DAG properties
            assert dag.dag_id == "spaceflights_weekly_model_training"
            assert dag.description is not None
            assert dag.schedule is not None
            
            # Check that DAG has tasks
            assert len(dag.tasks) > 0
            
        except Exception as e:
            pytest.fail(f"Weekly training DAG structure test failed: {e}")
    
    def test_dag_task_dependencies(self):
        """Test that DAGs have proper task dependencies"""
        try:
            import spaceflights_advanced_ml_pipeline
            
            dag = spaceflights_advanced_ml_pipeline.dag
            
            # Check that tasks have dependencies
            tasks_with_dependencies = [task for task in dag.tasks if task.downstream_task_ids]
            assert len(tasks_with_dependencies) > 0, "DAG should have tasks with dependencies"
            
        except Exception as e:
            pytest.fail(f"DAG task dependencies test failed: {e}")
    
    def test_dag_default_args(self):
        """Test that DAGs have proper default arguments"""
        try:
            import spaceflights_advanced_ml_pipeline
            
            dag = spaceflights_advanced_ml_pipeline.dag
            
            # Check default args
            assert dag.default_args is not None
            assert 'owner' in dag.default_args
            assert 'retries' in dag.default_args
            assert 'retry_delay' in dag.default_args
            
        except Exception as e:
            pytest.fail(f"DAG default args test failed: {e}")
    
    def test_dag_tags(self):
        """Test that DAGs have proper tags"""
        try:
            import spaceflights_advanced_ml_pipeline
            
            dag = spaceflights_advanced_ml_pipeline.dag
            
            # Check tags
            assert dag.tags is not None
            assert len(dag.tags) > 0
            
        except Exception as e:
            pytest.fail(f"DAG tags test failed: {e}")


class TestKedroOperator:
    """Test KedroOperator functionality"""
    
    def test_kedro_operator_import(self):
        """Test that KedroOperator can be imported"""
        try:
            from operators.kedro_operator import KedroOperator
            assert KedroOperator is not None
        except ImportError as e:
            pytest.fail(f"KedroOperator import failed: {e}")
    
    def test_kedro_operator_initialization(self):
        """Test KedroOperator initialization"""
        try:
            from operators.kedro_operator import KedroOperator
            
            operator = KedroOperator(
                task_id="test_task",
                package_name="spaceflights",
                pipeline_name="data_processing",
                node_name="test_node",
                project_path="/app"
            )
            
            assert operator.task_id == "test_task"
            assert operator.package_name == "spaceflights"
            assert operator.pipeline_name == "data_processing"
            assert operator.node_name == ["test_node"]
            
        except Exception as e:
            pytest.fail(f"KedroOperator initialization test failed: {e}")
    
    @patch('operators.kedro_operator.configure_project')
    @patch('operators.kedro_operator.KedroSession')
    def test_kedro_operator_execution(self, mock_session, mock_configure):
        """Test KedroOperator execution"""
        try:
            from operators.kedro_operator import KedroOperator
            
            # Mock the KedroSession
            mock_session_instance = MagicMock()
            mock_session.create.return_value.__enter__.return_value = mock_session_instance
            
            operator = KedroOperator(
                task_id="test_task",
                package_name="spaceflights",
                pipeline_name="data_processing",
                node_name="test_node",
                project_path="/app"
            )
            
            # Mock context
            mock_context = {}
            
            # Execute operator
            operator.execute(mock_context)
            
            # Verify that configure_project was called
            mock_configure.assert_called_once_with("spaceflights")
            
            # Verify that KedroSession.create was called
            mock_session.create.assert_called_once()
            
        except Exception as e:
            pytest.fail(f"KedroOperator execution test failed: {e}")


class TestDAGConfiguration:
    """Test DAG configuration and settings"""
    
    def test_dag_config_import(self):
        """Test that DAG config can be imported"""
        try:
            import config
            assert hasattr(config, 'DEFAULT_DAG_ARGS')
            assert hasattr(config, 'KEDRO_PACKAGE_NAME')
            assert hasattr(config, 'KEDRO_PROJECT_PATH')
            assert hasattr(config, 'TAGS')
        except ImportError as e:
            pytest.fail(f"DAG config import failed: {e}")
    
    def test_dag_config_values(self):
        """Test that DAG config has proper values"""
        try:
            import config
            
            # Test default args
            assert config.DEFAULT_DAG_ARGS is not None
            assert 'owner' in config.DEFAULT_DAG_ARGS
            assert 'retries' in config.DEFAULT_DAG_ARGS
            
            # Test Kedro config
            assert config.KEDRO_PACKAGE_NAME == "spaceflights"
            assert config.KEDRO_PROJECT_PATH is not None
            
            # Test tags
            assert config.TAGS is not None
            assert 'ML' in config.TAGS
            assert 'ETL' in config.TAGS
            
        except Exception as e:
            pytest.fail(f"DAG config values test failed: {e}")


class TestDAGValidation:
    """Test DAG validation and integrity"""
    
    def test_all_dags_have_unique_ids(self):
        """Test that all DAGs have unique IDs"""
        try:
            import spaceflights_advanced_ml_pipeline
            import spaceflights_daily_data_processing
            import spaceflights_ml_pipeline
            import spaceflights_on_demand
            import spaceflights_weekly_model_training
            
            dag_ids = [
                spaceflights_advanced_ml_pipeline.dag.dag_id,
                spaceflights_daily_data_processing.dag.dag_id,
                spaceflights_ml_pipeline.dag.dag_id,
                spaceflights_on_demand.dag.dag_id,
                spaceflights_weekly_model_training.dag.dag_id
            ]
            
            # Check that all DAG IDs are unique
            assert len(dag_ids) == len(set(dag_ids)), "All DAG IDs should be unique"
            
        except Exception as e:
            pytest.fail(f"DAG ID uniqueness test failed: {e}")
    
    def test_all_dags_have_start_date(self):
        """Test that all DAGs have start dates"""
        try:
            import spaceflights_advanced_ml_pipeline
            import spaceflights_daily_data_processing
            import spaceflights_ml_pipeline
            import spaceflights_on_demand
            import spaceflights_weekly_model_training
            
            dags = [
                spaceflights_advanced_ml_pipeline.dag,
                spaceflights_daily_data_processing.dag,
                spaceflights_ml_pipeline.dag,
                spaceflights_on_demand.dag,
                spaceflights_weekly_model_training.dag
            ]
            
            for dag in dags:
                assert dag.start_date is not None, f"DAG {dag.dag_id} should have a start date"
            
        except Exception as e:
            pytest.fail(f"DAG start date test failed: {e}")
    
    def test_all_dags_have_tasks(self):
        """Test that all DAGs have tasks"""
        try:
            import spaceflights_advanced_ml_pipeline
            import spaceflights_daily_data_processing
            import spaceflights_ml_pipeline
            import spaceflights_on_demand
            import spaceflights_weekly_model_training
            
            dags = [
                spaceflights_advanced_ml_pipeline.dag,
                spaceflights_daily_data_processing.dag,
                spaceflights_ml_pipeline.dag,
                spaceflights_on_demand.dag,
                spaceflights_weekly_model_training.dag
            ]
            
            for dag in dags:
                assert len(dag.tasks) > 0, f"DAG {dag.dag_id} should have tasks"
            
        except Exception as e:
            pytest.fail(f"DAG tasks test failed: {e}")

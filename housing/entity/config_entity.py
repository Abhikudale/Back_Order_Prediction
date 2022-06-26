from collections import namedtuple

DataIngestionConfig=namedtuple("DataIngestionConfig",
["dataset_download_url","tgz_download_dir","raw_data_dir","ingested_train_dir","ingested_test_dir"])

DataValidationConfig=namedtuple("DataValidationConfig",
['scheme_file_path'])

DataTransformationConfig=namedtuple("DataTransformationConfig",["add_bedroom_per_room",
                                                                "transformed_train_dir",
                                                                "transformed_testdir",
                                                                "preprocessed_object_file_path"])

ModelTrainingConfig=namedtuple("ModelTrainingConfig",["trained_model_file_path",
"base accuracy"])

ModelEvaluationConfig=namedtuple("ModelEvaluationConfig",["model_evaluation_file_path","time_stamp"])

ModelPusherConfig=namedtuple("ModelPusherConfig",["export_directoory_path"])

TrainingPipelineConfig=namedtuple("TrainingPipelineConfig",["artifact_dir"])
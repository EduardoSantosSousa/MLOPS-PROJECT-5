from kfp import dsl
from kubernetes.client import V1Volume, V1VolumeMount, V1SecretVolumeSource, V1EnvVar, V1Container
import kfp.compiler

def data_ingestion_op():
    op = dsl.ContainerOp(
        name="Data Ingestion",
        image="eduardosousa1493/my-mlops-app:latest",
        command=["python", "src/data_ingestion.py"]
    )

    # Monta o volume com a chave
    op.add_volume(
        V1Volume(
            name="gcp-sa-key",
            secret=V1SecretVolumeSource(secret_name="gcp-sa-key")
        )
    )

    op.container.add_volume_mount(
        V1VolumeMount(
            name="gcp-sa-key",
            mount_path="/app/credentials",
            read_only=True
        )
    )

    op.container.add_env_variable(
        V1EnvVar(
            name="GOOGLE_APPLICATION_CREDENTIALS",
            value="/app/credentials/credentials.json"
        )
    )

    # Adiciona o init container diretamente na operação
    op.add_init_container(
        V1Container(
            name="kfp-replacement-init-container",
            image="busybox:1.36.1",  # Versão atualizada e compatível
            command=['sh', '-c', 'echo "Init container substituído com sucesso"']
        )
    )

    return op


def data_processing_op():
    op = dsl.ContainerOp(
        name="Data Processing",
        image="eduardosousa1493/my-mlops-app:latest",
        command=["python", "src/data_processing.py"]
    )
    
    # Adiciona init container para esta operação também
    op.add_init_container(
        V1Container(
            name="kfp-replacement-init-container",
            image="busybox:1.36.1",
            command=['sh', '-c', 'echo "Init container substituído com sucesso"']
        )
    )
    return op


def model_training_op():
    op = dsl.ContainerOp(
        name="Model Training",
        image="eduardosousa1493/my-mlops-app:latest",
        command=["python", "src/model_training.py"]
    )
    
    # Adiciona init container para esta operação também
    op.add_init_container(
        V1Container(
            name="kfp-replacement-init-container",
            image="busybox:1.36.1",
            command=['sh', '-c', 'echo "Init container substituído com sucesso"']
        )
    )
    return op


@dsl.pipeline(
    name="MLOPS Pipeline",
    description="This is my first ever kubeflow pipeline"
)
def mlops_pipeline():
    ingestion = data_ingestion_op()
    processing = data_processing_op().after(ingestion)
    training = model_training_op().after(processing)


# Compile
if __name__ == "__main__":
    kfp.compiler.Compiler().compile(
        mlops_pipeline, "mlops_pipeline.yaml"
    )
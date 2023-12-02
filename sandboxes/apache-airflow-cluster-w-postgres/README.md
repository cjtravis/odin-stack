# Apache Airflow Cluster with Postgres Project Setup
Welcome to your Apache Airflow project! This guide will help you set up and manage your Airflow environment using Docker Compose. Whether you're new to Airflow or an experienced user, this project makes it easy to get started quickly.

## Getting Started
Before we begin, make sure you have Docker and Docker Compose installed on your machine. If you haven't already, you can download and install them here:

Docker: Install Docker
Docker Compose: Install Docker Compose

### Step 1: Clone the Repository
First, clone this repository to your local machine by running the following commands in your terminal:

```bash
git clone <repository_url>
cd projects/apache-airflow-cluster-w-postgres
```

### Step 2: Build Docker Compose Services
Next, let's build the Docker Compose services for your Airflow project. This step will prepare the necessary containers and dependencies:

```bash
docker-compose build
```

### Step 3: Initialize Airflow Database
Now, it's time to initialize the Airflow database. This is a crucial step in setting up your Airflow environment:

```bash
docker-compose up airflow-init
```

### Step 4: Start Airflow and Other Services
To start your Airflow cluster along with other services, simply run the following command:

```bash
docker-compose up
```

### Verifying Container Status
To check the status and health of the Docker Compose containers, you can use the following command:

```bash
docker-compose ps
```

This command will display the current state of each container, including whether they are running and healthy.

## The Dockerfile

The Dockerfile is used to build a custom Docker image for Apache Airflow. This image is tailored to your project's requirements and includes the necessary Python dependencies specified in the `requirements.txt` file. It ensures that your Airflow environment is consistent and reproducible.

## Understanding docker-compose.yml
Now, let's break down what each service in the `docker-compose.yml` is doing:

### x-airflow-common

The `x-airflow-common` section is a YAML extension, often referred to as a "YAML anchor," that defines a common set of configurations and environment variables shared across multiple services or containers in your Apache Airflow environment.

This common configuration helps streamline the setup and maintain consistency across various Airflow-related containers. Here's how the `x-airflow-common` section supports Airflow's needs:

  - **Configuration Reusability**: Instead of duplicating environment variables and settings in each container definition, you define them once in the `x-airflow-common` section. This promotes consistency and simplifies maintenance.

  - **Environment Variables**: Environment variables defined within `x-airflow-common` are inherited by services that reference it. These variables often include critical Airflow configuration settings, such as database connection details, Celery executor configuration, and logging options.


  - **Volume Mounts**: Shared volume mounts allow multiple services to access common directories or files. For example, mounting the `./dags` directory from the host into containers ensures that DAG definitions are accessible to all Airflow services.

    - `./dags` - you can put your DAG files here.
    - `./logs` - contains logs from task execution and scheduler.
    - `./plugins` - you can put your custom plugins here. 

  - **User Configuration**: Specifying user and group IDs in the `user` field ensures consistent ownership and permissions for files created within containers, which is crucial for Airflow's proper functioning.

  The `x-airflow-common` section promotes configuration reusability and consistency across services, reducing potential configuration errors and simplifying updates.

- **Environment Variables**: Environment variables and configurations defined within `x-airflow-common` are inherited by services that reference it.

- **Volumes**: Shared volumes, if defined within `x-airflow-common`, are accessible to services referencing this extension.

- **User Configuration**: The `user` field defines the user and group IDs for processes within containers, ensuring consistent ownership and permissions for files created.

You can customize the `x-airflow-common` section to include or modify environment variables, volumes, and user configurations as needed to match the requirements of your specific Airflow project. It serves as a central configuration hub for maintaining consistency and simplifying your Airflow setup.


### postgres

The PostgreSQL database is a critical component in your Apache Airflow environment, serving as the metadata database. It is responsible for storing and managing metadata related to your workflows, DAGs, task states, job execution details, and more.
  
Apache Airflow relies on a metadata database to maintain information about the state and history of your workflow automation tasks. This includes details about DAGs, task dependencies, execution times, logs, and much more. The PostgreSQL database is used to persist this metadata, allowing Airflow to:

- Keep track of DAGs and their structures.
- Record task execution history, including success, failure, and retries.
- Maintain a history of execution dates, ensuring tasks run on schedule.
- Provide a clear view of task dependencies and execution order.
- Store logs and task-specific details for troubleshooting and auditing.

By using PostgreSQL as the metadata database, your Airflow environment becomes highly reliable and scalable, making it easier to manage and monitor complex workflows.

- **Environment Variables**: 
  - `POSTGRES_USER`: The username for PostgreSQL.
  - `POSTGRES_PASSWORD`: The password for PostgreSQL.
  - `POSTGRES_DB`: The name of the Airflow database.

- **Ports**: Maps port 5432 inside the container to port 5432 on your host machine.
- **Volumes**: Mounts a local directory for persistent data storage.
- **Healthcheck**: Ensures that PostgreSQL is ready to accept connections.
- **Restart**: Set to "always" to automatically restart the service if it stops unexpectedly.

For more detailed information on how Apache Airflow uses a metadata database, you can refer to the official Airflow documentation on [Metadata Database](https://airflow.apache.org/docs/apache-airflow/stable/concepts/metadatabase.html).

You can further customize the PostgreSQL configuration to meet your specific requirements by modifying the `docker-compose.yml` file.

### redis

The Redis service plays a vital role in your Apache Airflow environment by serving as the message broker and result backend for the Celery executor.

Apache Airflow uses Celery as an executor to distribute and execute tasks in parallel. To efficiently manage the distribution of tasks and the communication between Airflow components, it relies on a message broker and a result backend. Redis serves as both in this context:

  - **Message Broker**: Redis acts as the message broker, facilitating communication between the Airflow scheduler and the Celery workers. When a task is ready to be executed, it is placed in a message queue in Redis. The Celery workers monitor this queue and pick up tasks for execution as soon as they become available, ensuring efficient task distribution and execution.

  - **Result Backend**: Redis also acts as the result backend, storing the results of task execution. After a Celery worker completes a task, it stores the result in Redis. Airflow can then retrieve these results and update the status of tasks, allowing you to monitor the progress and outcome of your workflow.

  By using Redis as the message broker and result backend, your Airflow environment gains the ability to distribute and execute tasks in a scalable and reliable manner, ensuring efficient task scheduling and monitoring.

- **Ports**: Maps port `6379` inside the container to port `6379` on your host machine.
- **Healthcheck**: Checks if Redis is responsive.
- **Restart**: Set to "always" to automatically restart the service if it stops unexpectedly.

For more detailed information on how Apache Airflow uses Celery with a message broker and result backend, you can refer to the official Airflow documentation on [Celery Executor](https://airflow.apache.org/docs/apache-airflow/stable/executor/celery.html).

You can further customize the Redis configuration to meet your specific requirements by modifying the `docker-compose.yml` file.


### airflow-webserver

The `airflow-webserver` container is a key component of your Apache Airflow environment, serving as the web-based user interface for managing and monitoring your DAGs, tasks, and workflows.

The web server provided by this container allows you to interact with Airflow through a user-friendly web interface. Here's how it supports Airflow's needs:

  - **Web-Based DAG Management**: You can use the web interface to create, edit, and manage your DAGs visually. This makes it easier to design and maintain complex workflows.

  - **Task Monitoring**: The web UI provides a real-time view of the status of your tasks, allowing you to monitor their progress and troubleshoot any issues.

  - **Execution Controls**: You can trigger DAG runs, pause/resume DAGs, and view detailed task logs directly from the web interface.

  - **Scheduler Interaction**: The web server communicates with the scheduler to ensure tasks are executed according to your schedule and dependencies.

  - **User Authentication**: It supports user authentication and role-based access control, allowing you to restrict access to sensitive workflows and data.

  The `airflow-webserver` container is essential for providing a user-friendly interface for managing your Airflow environment and ensuring that your workflows are executed reliably.

**Command**: Starts the web server.
**Ports**: Maps port `8080` inside the container to port `8080` on your host machine, making the Airflow web UI accessible through [http://localhost:8080](http://localhost:8080).
**Healthcheck**: Checks if the web server is responsive.
**Restart**: Set to "always" to automatically restart the service if it stops unexpectedly.

You can access the Airflow Web UI by navigating to [http://localhost:8080](http://localhost:8080) in your web browser.

Feel free to customize the `airflow-webserver` container's configuration or enable additional features as needed by modifying the `docker-compose.yml` file.

### airflow-scheduler

The `airflow-scheduler` container is a critical component of your Apache Airflow environment, responsible for scheduling the execution of your workflows, known as Directed Acyclic Graphs (DAGs).

The scheduler plays a central role in ensuring that your tasks are executed at the right time, respecting dependencies and constraints. Here's how the `airflow-scheduler` container supports Airflow's needs:

  - **DAG Scheduling**: It continuously monitors the DAGs you've defined and schedules the execution of tasks based on their dependencies and the specified schedule intervals.

  - **Dependency Resolution**: The scheduler determines the order in which tasks should be executed by analyzing their dependencies. It ensures that tasks are not executed until their upstream tasks have completed successfully.

  - **Concurrency Control**: It manages the concurrency of task execution, allowing you to control how many tasks can run simultaneously to avoid resource bottlenecks.

  - **Error Handling**: If a task fails, the scheduler can be configured to handle retries and task failures according to your specifications.

  - **Dynamic Workload**: The scheduler adapts to changes in your DAGs in real-time, making it possible to add or modify tasks without interrupting ongoing executions.

  The `airflow-scheduler` container is essential for orchestrating the execution of your workflows, ensuring that they run efficiently and according to your specified schedules and dependencies.

- **Command**: Starts the scheduler.
- **Restart**: Set to "always" to automatically restart the service if it stops unexpectedly.

You can customize the behavior and configuration of the `airflow-scheduler` container to meet your specific workflow scheduling requirements by modifying the `docker-compose.yml` file.

### airflow-worker

The `airflow-worker` container is a crucial component of your Apache Airflow environment, responsible for executing tasks defined within your Directed Acyclic Graphs (DAGs).

The worker plays a pivotal role in ensuring that your tasks are executed efficiently, reliably, and in parallel. Here's how the `airflow-worker` container supports Airflow's needs:

  - **Task Execution**: It continuously monitors the task queue for incoming tasks to execute. When a task becomes available, the worker picks it up and runs it in a separate process or container.

  - **Parallel Execution**: Multiple worker instances can be deployed to execute tasks concurrently, allowing you to scale the execution of tasks to meet your workload demands.

  - **Task Isolation**: Tasks are executed within isolated environments, preventing interference between different tasks. This isolation ensures that task execution is consistent and reliable.

  - **Error Handling**: Workers handle task execution errors, including retries and logging, based on the configuration you've defined in your DAGs.

  - **Dynamic Scaling**: You can adjust the number of worker instances to scale horizontally, making it possible to handle larger workloads as needed.

  The `airflow-worker` container is essential for efficiently executing the tasks defined in your workflows (DAGs) and ensuring that they are completed successfully.

- **Command**: Starts the Celery worker, which listens for and executes tasks.
- **Restart**: Set to "always" to automatically restart the service if it stops unexpectedly.

You can configure and scale the `airflow-worker` container to match the workload requirements of your Apache Airflow environment by modifying the `docker-compose.yml` file.

### airflow-init

The `airflow-init` container performs essential initialization tasks and ensures that your Airflow environment is ready to run workflows. Here's how the `airflow-init` container supports Airflow's needs:

  - **Database Setup**: It takes care of setting up the Airflow metadata database, including initializing the database schema and ensuring that it's ready for use by other Airflow components.

  - **User Creation**: The `airflow-init` container creates the default user for the Airflow Web UI. This user is used to log in and manage your Airflow environment.

  - **Configuration**: It initializes various Airflow configuration settings, including those related to remote logging, DAGs pausing at creation, example DAG loading, and more, ensuring that Airflow operates according to your project's requirements.

  - **Security**: The container can set up authentication and encryption settings, including Fernet key configuration and remote log encryption options, to secure your Airflow environment.

  The `airflow-init` container ensures that your Airflow instance is properly configured and ready to use, making it an essential step in setting up your Airflow environment.

- **Command**: Runs the Airflow version command and performs initialization tasks.
- **Environment Variables**: Various environment variables for Airflow configuration can be set within the container.
- **Restart**: Set to "always" to automatically restart the service if it stops unexpectedly.

You can customize the initialization process and environment variables to meet your specific Airflow project requirements by modifying the `docker-compose.yml` file.

### flower

The `flower` container is an optional yet valuable component of your Apache Airflow environment, providing a real-time monitoring and administration interface for your Celery workers and tasks.

Flower is a web-based tool that allows you to visualize and manage the status of your Celery workers, tasks, and queues. Here's how the `flower` container supports Airflow's needs:

  - **Real-Time Monitoring**: Flower provides a real-time dashboard that displays information about your Celery workers, including their current activity, resource usage, and task execution progress.

  - **Task Management**: You can view the list of active tasks, inspect task details, and even revoke or terminate tasks from the Flower web interface, giving you fine-grained control over task execution.

  - **Queue Inspection**: Flower allows you to see the state of your task queues, making it easier to identify potential bottlenecks or issues in your workflow.

  - **Security**: Flower supports basic authentication, allowing you to restrict access to the monitoring interface, ensuring that only authorized users can view and manage your Celery workers and tasks.

  The `flower` container enhances the observability and management capabilities of your Airflow environment, making it easier to monitor task execution and troubleshoot issues.

- **Command**: Starts the Flower web interface for monitoring Celery workers.
- **Ports**: Maps port `5555` inside the container to port `5555` on your host machine, making the Flower web interface accessible through [http://localhost:5555](http://localhost:5555).
- **Healthcheck**: Checks if the Flower interface is responsive.
- **Restart**: Set to "always" to automatically restart the service if it stops unexpectedly.

You can access the Flower web interface by navigating to [http://localhost:5555](http://localhost:5555) in your web browser. 

Customize Flower's configuration and enable authentication to suit your monitoring and security requirements by modifying the `docker-compose.yml` file.

### networks

The `networks` section in the `docker-compose.yml` file defines and configures the networks used by the containers in your Apache Airflow environment. It ensures that the various containers can communicate with each other and, in some cases, with external resources.

Networks are essential for facilitating communication and data exchange between different components of your Airflow setup. Here's how the `networks` section supports Airflow's needs:

  - **Isolation**: By defining separate networks, you can isolate specific components of your Airflow environment. For example, the `airflow_network` network is used to connect all Airflow-related containers, isolating them from other containers running on your host machine.

  - **Inter-Container Communication**: Networks enable containers to communicate with each other using DNS names. For example, the `airflow-webserver` container can connect to the `postgres` container using the hostname `postgres`, allowing Airflow services to interact seamlessly.

  - **Resource Sharing**: Networks provide a mechanism for sharing resources, such as databases (in the case of `postgres`), message brokers (in the case of `redis`), and external services, among the various components of your Airflow environment.

  Properly configured networks ensure that your Airflow containers can work together effectively, ensuring data flow, task execution, and communication within your environment.

The `driver` specifies the network driver used for the network. In this case, it's set to `bridge`.

  **Implications of Using the `bridge` Driver**:

  - **Isolation**: The `bridge` driver creates a private internal network that is isolated from the host machine's network. This isolation provides a secure environment for your Airflow containers, ensuring that their communication doesn't interfere with or expose services running on the host.

  - **Private DNS**: Containers within the `bridge` network can resolve each other's DNS names, allowing for easy and consistent communication between containers. For example, the `airflow-webserver` container can reach the `postgres` container using the hostname `postgres`.

  - **External Accessibility**: While the `bridge` network isolates containers, it's possible to expose specific container ports to the host machine or external networks as needed. This allows you to control which services are accessible from outside the container environment.

  - **Default for Isolation**: The `bridge` driver is often the default choice for isolating containers within a Docker Compose project. It strikes a balance between security and convenience, making it suitable for most use cases.

In summary, the `networks` section with the `bridge` driver ensures proper isolation, secure communication, and controlled external accessibility for the containers in your Apache Airflow environment. It helps maintain a robust and reliable environment for orchestrating and managing your workflows.


## Accessing Airflow Web UI
Once the services are up and running, you can access the Airflow Web UI by navigating to http://localhost:8080 in your web browser. Here, you can manage and monitor your Airflow DAGs, tasks, and workflows.

## Customizing Your Airflow Setup
Feel free to customize your Airflow environment by modifying the docker-compose.yml file and adding your DAGs in the dags directory. This project provides a flexible foundation for your workflow automation needs.

## Custom Dockerfile and Requirements
If you need to customize your Airflow image to use a different base image, you can modify the included Dockerfile. Additionally, your project's Python dependencies are specified in the requirements.txt file. Customize these to meet your environment requirements.
```
pandas
selenium
bs4
pymongo
requests
swifter
numpy
lxml
flask-bcrypt
boto3
apache-airflow-providers-amazon
apache-airflow-providers-microsoft-azure
```
Feel free to add or remove dependencies as needed for your specific project requirements.

Enjoy your Airflow journey! 🚀
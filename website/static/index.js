function deleteTask(taskId) {
    fetch("/deleteTask", {
      method: "POST",
      body: JSON.stringify({ taskId: taskId }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }
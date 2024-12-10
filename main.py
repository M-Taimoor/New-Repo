from task import add

# Call the task asynchronously (it runs in the background)
result = add.apply_async((4, 6))

# You can check if the task is finished and get the result
print('Task result:', result.get())

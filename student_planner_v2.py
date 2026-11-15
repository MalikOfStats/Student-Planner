# Name: Abdulmalik Mubarak Al-Dosari | Student ID: 444102285 | Section: 91885

def display_menu():
    print("\n--- ACADEMIC TASK PLANNER ---")
    print("****************************************")
    print("1. Add a task")
    print("2. Edit a task")
    print("3. Delete a task")
    print("4. Find a task by ID")
    print("5. Search tasks by title keywords")
    print("6. List all tasks")
    print("7. List tasks by course")
    print("8. List tasks by priority")
    print("9. Mark a task as completed")
    print("10. View task summary")
    print("11. Exit")
    print("****************************************")

def _get_input(msg):
    val = input(msg).strip()
    while not val:
        print("Invalid input: This field is required and cannot be left empty.")
        val = input(msg).strip()
    return val

def _validate_date(date_str):
    chunks = date_str.split("/")
    if len(chunks) != 3:
        return False
    if len(chunks[0]) != 2 or len(chunks[1]) != 2 or len(chunks[2]) != 4:
        return False
    for seg in chunks:
        if not all(c in "0123456789" for c in seg):
            return False
    return True

def read_due_date():
    user_date = input("Enter due date (DD/MM/YYYY): ").strip()
    while not _validate_date(user_date):
        print("Invalid format: Please enter the date as DD/MM/YYYY using numbers only.")
        user_date = input("Enter due date (DD/MM/YYYY): ").strip()
    return user_date

def read_priority():
    selection = input("Select priority (1=High, 2=Medium, 3=Low): ").strip()
    while selection not in ("1", "2", "3"):
        print("Invalid selection: Please enter 1, 2, or 3.")
        selection = input("Select priority (1=High, 2=Medium, 3=Low): ").strip()
    
    mapping = {"1": "High", "2": "Medium", "3": "Low"}
    return mapping[selection]

def read_task_id():
    raw_text = input("Task ID: ").strip()
    if not raw_text or not all(c in "0123456789" for c in raw_text):
        print("Invalid ID: Must be a positive number using digits 0-9.")
        return None
    parsed_id = int(raw_text)
    if parsed_id <= 0:
        print("Invalid ID: Must be greater than zero.")
        return None
    return parsed_id

def add_task(tasks, next_task_id):
    t_title = _get_input("Enter task title: ")
    t_course = _get_input("Enter course code/name: ")
    t_date = read_due_date()
    t_pri = read_priority()
    
    new_task = {
        "id": next_task_id,
        "title": t_title,
        "course": t_course,
        "due_date": t_date,
        "priority": t_pri,
        "status": "Pending"
    }
    tasks.append(new_task)
    print(f"Done! Task created with ID #{next_task_id}.")
    return next_task_id + 1

def find_task_by_id(tasks, task_id):
    for item in tasks:
        if item["id"] == task_id:
            return item
    return None

def display_task(task):
    print(f"ID: {task['id']} | Status: {task['status']}")
    print(f"Title: {task['title']}")
    print(f"Course: {task['course']} | Due: {task['due_date']} | Priority: {task['priority']}")
    print("~" * 40)

def edit_task(tasks):
    t_id = read_task_id()
    if t_id is None:
        return
    target_task = find_task_by_id(tasks, t_id)
    if not target_task:
        print("No task exists with that ID.")
        return
        
    print("Select field to update:\n1. Title\n2. Course\n3. Due date\n4. Priority\n5. Cancel")
    opt = input("Option: ").strip()
    
    if opt == "5":
        print("Update aborted.")
        return
    elif opt == "4":
        target_task["priority"] = read_priority()
    elif opt == "3":
        target_task["due_date"] = read_due_date()
    elif opt == "2":
        target_task["course"] = _get_input("New course code/name: ")
    elif opt == "1":
        target_task["title"] = _get_input("New task title: ")
    else:
        print("Invalid option selected.")
        return
    print("Changes saved successfully.")

def delete_task(tasks):
    t_id = read_task_id()
    if t_id is None:
        return
    target_task = find_task_by_id(tasks, t_id)
    if not target_task:
        print("No task exists with that ID.")
    else:
        tasks.remove(target_task)
        print("The task has been removed.")

def search_tasks_by_title(tasks):
    query = input("Search keywords (separated by spaces): ").strip()
    if not query:
        print("Invalid search: Please enter at least one keyword.")
        return
    
    keywords = query.lower().split()
    matched_any = False
    
    for item in tasks:
        title_lower = item["title"].lower()
        match_all = True
        for kw in keywords:
            if kw not in title_lower:
                match_all = False
                break
        if match_all:
            display_task(item)
            matched_any = True
            
    if not matched_any:
        print("No matching tasks found for those keywords.")

def list_all_tasks(tasks):
    if not tasks:
        print("Your task list is currently empty.")
        return
    print("\n=== Current Tasks ===")
    for item in tasks:
        display_task(item)

def list_tasks_by_course(tasks):
    c_name = _get_input("Enter course code/name to filter: ")
    found_flag = False
    for item in tasks:
        if item["course"].lower() == c_name.lower():
            display_task(item)
            found_flag = True
    if not found_flag:
        print("No tasks recorded for this course.")

def list_tasks_by_priority(tasks):
    p_level = read_priority()
    found_flag = False
    for item in tasks:
        if item["priority"] == p_level:
            display_task(item)
            found_flag = True
    if not found_flag:
        print("No tasks match the selected priority.")

def mark_task_completed(tasks):
    t_id = read_task_id()
    if t_id is None:
        return
    target_task = find_task_by_id(tasks, t_id)
    if not target_task:
        print("No task exists with that ID.")
    elif target_task["status"] == "Completed":
        print("This task was already marked as completed.")
    else:
        target_task["status"] = "Completed"
        print(f"Great job! Task #{t_id} is now completed.")

def show_summary(tasks):
    total_count = len(tasks)
    comp_count = sum(1 for item in tasks if item["status"] == "Completed")
    pend_count = total_count - comp_count
    
    print("\n=== Progress Overview ===")
    print(f"Total tasks: {total_count}")
    print(f"Pending tasks: {pend_count}")
    print(f"Completed tasks: {comp_count}")
    
    if total_count == 0:
        print("Completion percentage: 100%")
    else:
        pct = (comp_count / total_count) * 100
        print(f"Completion percentage: {pct:.1f}%")

def _handle_find_id(tasks):
    t_id = read_task_id()
    if t_id is not None:
        res = find_task_by_id(tasks, t_id)
        if res:
            print("\n=== Found Task ===")
            display_task(res)
        else:
            print("No task exists with that ID.")

def main():
    tasks = []
    next_task_id = 1
    
    actions = {
        "2": edit_task,
        "3": delete_task,
        "4": _handle_find_id,
        "5": search_tasks_by_title,
        "6": list_all_tasks,
        "7": list_tasks_by_course,
        "8": list_tasks_by_priority,
        "9": mark_task_completed,
        "10": show_summary
    }
    
    while True:
        display_menu()
        user_choice = input("Select an option (1-11): ").strip()
        
        if user_choice == "11":
            print("See you later! Best of luck with your studies.")
            break
        elif user_choice == "1":
            next_task_id = add_task(tasks, next_task_id)
        elif user_choice in actions:
            actions[user_choice](tasks)
        else:
            print("Invalid selection: Please pick a number between 1 and 11.")

if __name__ == "__main__":
    main()

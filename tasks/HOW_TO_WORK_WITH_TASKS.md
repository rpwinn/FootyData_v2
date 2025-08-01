# How to Work with Tasks

This guide explains the complete workflow for managing tasks in the FootyData_v2 project. Follow these 5 steps to effectively create, work on, and complete tasks.

## 📋 Overview

The task management system uses markdown files in organized directories to track progress. Each task is a self-contained unit with clear objectives, acceptance criteria, and implementation steps.

## 🎯 The 5-Step Workflow

### 1. Create Tasks

**When to create a task:**
- Breaking down large goals into manageable pieces
- Identifying specific work that needs to be done
- Planning new features or improvements

**How to create a task:**

1. **Use the template:**
   ```bash
   cp tasks/templates/task_template.md tasks/active/TASK-XXX_[description].md
   ```

2. **Fill in the details:**
   - **Objective**: What needs to be accomplished
   - **Acceptance Criteria**: How you'll know it's done
   - **Implementation Steps**: Step-by-step breakdown
   - **Priority**: HIGH/MEDIUM/LOW
   - **Estimated Time**: Realistic time estimate

3. **Example task creation:**
   ```bash
   cp tasks/templates/task_template.md tasks/active/TASK-002_setup_database_tables.md
   ```

4. **Update the task index:**
   - Add the new task to `tasks/README.md` under "Current Active Tasks"

### 2. Do Work

**When working on a task:**

1. **Start with the task card:**
   - Read the objective and acceptance criteria
   - Review the implementation steps
   - Understand the scope and requirements

2. **Follow the implementation steps:**
   - Work through each step systematically
   - Update progress as you go
   - Document any discoveries or issues

3. **Keep the task card updated:**
   - Mark completed steps
   - Add notes about progress
   - Document any blockers or changes

4. **Example work session:**
   ```bash
   # Read the task
   cat tasks/active/TASK-002_setup_database_tables.md
   
   # Work on the implementation
   # ... do the actual work ...
   
   # Update progress in the task card
   # Mark completed steps, add notes
   ```

### 3. Update Tasks

**When to update tasks:**
- Progress is made on implementation steps
- New information is discovered
- Requirements change
- Blockers are encountered

**How to update tasks:**

1. **Mark progress:**
   - ✅ Check off completed implementation steps
   - 📝 Add notes about what was accomplished
   - ⚠️ Document any issues or blockers

2. **Update status if needed:**
   - Move to `tasks/blocked/` if waiting for dependencies
   - Move to `tasks/active/` if unblocked
   - Update priority if circumstances change

3. **Example task update:**
   ```markdown
   ## Implementation Steps
   
   ✅ 1. Audit current database schema
   ✅ 2. Create dimension table scripts
   ⏳ 3. Create fact table scripts
   📝 Note: Discovered we need additional indexes for performance
   ```

4. **Update the task index:**
   - Reflect current status in `tasks/README.md`

### 4. Finish Work

**When work is complete:**

1. **Verify completion:**
   - Review all acceptance criteria
   - Test the implementation
   - Ensure all requirements are met

2. **Document the work:**
   - Update the task card with final notes
   - Document any important discoveries
   - Note any follow-up work needed

3. **Prepare for completion:**
   - Ensure all files are properly organized
   - Update any related documentation
   - Test the implementation thoroughly

4. **Example completion preparation:**
   ```bash
   # Verify all acceptance criteria are met
   # Test the implementation
   # Update any related documentation
   # Ensure files are in the right places
   ```

### 5. Complete Tasks

**When a task is fully complete:**

1. **Move the task card:**
   ```bash
   mv tasks/active/TASK-XXX_[description].md tasks/completed/
   ```

2. **Update the task index:**
   - Move from "Current Active Tasks" to "Recently Completed Tasks"
   - Update status to "DONE"
   - Add completion date and summary

3. **Archive related files:**
   - Move any task-specific files to appropriate locations
   - Update project documentation if needed
   - Clean up temporary files

4. **Example completion:**
   ```bash
   # Move the task card
   mv tasks/active/TASK-002_setup_database_tables.md tasks/completed/
   
   # Update the README
   # Move from active to completed section
   # Add completion summary
   ```

## 📁 Directory Structure

```
tasks/
├── README.md                    # Main task index
├── HOW_TO_WORK_WITH_TASKS.md   # This guide
├── templates/                   # Task templates
│   └── task_template.md        # Standard task template
├── active/                     # Currently active tasks
├── completed/                  # Finished tasks
├── blocked/                    # Tasks waiting for dependencies
└── backlog/                    # Future tasks
```

## 🎯 Task Status Flow

```
Backlog → Active → [Blocked] → Active → Completed
   ↓         ↓         ↓         ↓         ↓
Create    Do Work   Update    Finish    Archive
Tasks     Tasks     Work      Tasks
```

## 📝 Best Practices

### Creating Tasks
- **Be specific**: Clear, measurable objectives
- **Break down**: Small, manageable steps
- **Estimate realistically**: Include buffer time
- **Set clear criteria**: How you'll know it's done

### Working on Tasks
- **Start with the card**: Read before beginning
- **Update regularly**: Keep progress current
- **Document discoveries**: Notes help future work
- **Stay focused**: One task at a time

### Updating Tasks
- **Be honest**: Accurate status helps planning
- **Document blockers**: Don't let tasks stall
- **Note changes**: Requirements evolve
- **Keep it current**: Regular updates

### Completing Tasks
- **Verify thoroughly**: Don't rush completion
- **Document outcomes**: What was accomplished
- **Clean up**: Proper file organization
- **Archive properly**: Move to completed

## 🔄 Example Workflow

### Creating TASK-003
```bash
# 1. Create the task
cp tasks/templates/task_template.md tasks/active/TASK-003_implement_data_validation.md

# 2. Fill in details
# Edit the task card with objective, criteria, steps

# 3. Update index
# Add to tasks/README.md active tasks list
```

### Working on TASK-003
```bash
# 1. Read the task
cat tasks/active/TASK-003_implement_data_validation.md

# 2. Do the work
# Follow implementation steps

# 3. Update progress
# Mark completed steps, add notes
```

### Completing TASK-003
```bash
# 1. Verify completion
# Test implementation, check criteria

# 2. Move task card
mv tasks/active/TASK-003_implement_data_validation.md tasks/completed/

# 3. Update index
# Move from active to completed in README.md
```

## 🚨 Common Mistakes

### ❌ Don't:
- Create tasks without clear objectives
- Work without reading the task card
- Forget to update progress
- Leave tasks in active when blocked
- Rush completion without verification

### ✅ Do:
- Create specific, measurable tasks
- Read and understand before starting
- Update progress regularly
- Move blocked tasks to blocked/
- Verify completion thoroughly

## 📊 Tracking Progress

- **Active tasks**: Currently being worked on
- **Completed tasks**: Recently finished work
- **Blocked tasks**: Waiting for dependencies
- **Backlog**: Future work planned

This system ensures that work is organized, trackable, and properly archived when complete.

---

*Last Updated: [Current Date]* 
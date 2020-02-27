select * from title;
select * from department;
select * from employee;

delete from title;

select emp_no, emp_name, title, ifnull(manager,0) as manager, salary, dept, if(pass!=null, 'null', 'null') as pass, hire_date, gender, pic  from employee;
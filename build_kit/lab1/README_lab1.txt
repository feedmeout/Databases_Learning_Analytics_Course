Lab 1 (Week 2, Part 2) - data, notebooks and generator. ALL DATA ARE SIMULATED.

data/students_last.csv            last year's cohort (312), one row per student, outcomes included
data/students_this_week4.csv      this year's cohort (298) at the end of week 4, no outcomes
data/submissions_last.csv         one row per attempted exercise: student_id, sheet, exercise, week, late, sequence (E/S)
data/submissions_this_week4.csv   the same for this year's cohort, on-time submissions of weeks 1-4 only
data/logins_last.csv              eclass logins per student and week (w1..w13)
data/logins_this_week4.csv        the same for this year's cohort, w1..w4
data/teacher/                     TEACHER ONLY: full files with the latent skill and commitment and this year's outcomes

Lab1_notebook_student.ipynb       optional, for after the session; data embedded, runs in Google Colab (File > Upload notebook)
Lab1_notebook_teacher.ipynb       TEACHER ONLY: also scores any rule on this year's cohort and shows what each trace measures
simulate.py                       the generator (seeds 36 and 71); parameters are documented on page 2 of the teacher key

Columns of students_*.csv: enrolment (first/repeat), works (0/1), logins_w1_4, submissions_w1_4, EE ES SE SS (transition counts,
on-time submissions of weeks 1-4), p_ES_w1_4 (empty when fewer than 4 transitions start from E), sheets_on_time_w1_4 (0-4),
sheets_semester (0-12), midterm, exam, no_show, passed, last_active_week.

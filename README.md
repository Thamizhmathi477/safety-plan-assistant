🏮 RescuePlan
A lantern for hard nights.
Built by Thamizhmathi, Arunai Engineering College, for RescueHacks 2026
(Mental Health Support track).
Why I built this
I came across the Student Depression Dataset on Kaggle
while working on an unrelated project, and the numbers stayed with me — 27,901
Indian students, and depression showing up in nearly 6 out of 10 of them.
I trained a quick model on it (Logistic Regression, ~91.8% AUC) just to see what
actually correlated most with depression. Academic pressure and financial stress
came out near the top, right alongside a history of suicidal thoughts. None of
that surprised me, honestly — most students I know carry some version of that
stress. What struck me was how few of us have ever sat down and actually made a
plan for what to do when things get hard, before they get hard.
That's what RescuePlan tries to be: something you fill out on a calm day, so it's
already there on a bad one.
What it does
RescuePlan walks a student through six short steps, based on the Stanley-Brown
Safety Planning Intervention — the same framework crisis counselors actually
use:
Warning signs
Coping strategies
Supportive people & places
People to ask for help
Professional contacts
Making your environment safer
At the end, you get a plan you can download and keep. Verified India crisis
helplines (Tele-MANAS, Vandrevala Foundation, iCALL, KIRAN, and 112) are visible
the entire time, not buried in a menu.
There's also a Quick Self Check-in — a few honest questions about how things
have been going lately (sleep, pressure, stress). I deliberately did not turn
this into a risk score or percentage. Early on I looked at building exactly that,
and realized a model that's ~92% accurate on average can still be badly wrong for
one specific person — and telling someone "Low Risk" after they've just told you
about suicidal thoughts would be actively dangerous, not helpful. So instead, any
mention of suicidal thoughts skips scoring entirely and goes straight to real
crisis resources.
Why it's bilingual
I grew up speaking Tamil, and I know plenty of students who think and process
things more clearly in Tamil than in English, especially when it's something
personal. So the whole flow — including the downloadable plan — works in both
languages, not just the UI labels.
Built with
Python + Streamlit
scikit-learn (for the underlying analysis of the depression dataset)
Deployed on Streamlit Community Cloud
Data source
Student Depression Dataset,
Kaggle, n=27,901. Used only to understand aggregate patterns during development —
the deployed app doesn't store or process any user's personal data.
Disclaimer
RescuePlan is a self-guided planning tool, not a diagnosis and not a replacement
for professional care. If you're in immediate danger, please contact emergency
services (112 in India) or someone you trust right now.
Where I'd take this next
Pilot it with my college's counseling cell to see if students actually use it
Add Hindi and other regional languages
A gentle, optional reminder to revisit the plan every so often — safety plans
work best when they're kept up to date, not written once and forgotten
Talk to an actual counselor about whether the check-in questions are asking the
right things, since I built these off my own instincts, not clinical training

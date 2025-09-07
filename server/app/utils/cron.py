from datetime import datetime, timedelta, timezone
from flask_apscheduler import APScheduler
from server.db.db_session import create_session
from server.db.models.__all_models import Expense

scheduler = APScheduler()


def check_periodic_expenses():
    db_sess = create_session()
    now = datetime.now(timezone.utc)
    print(f"[CRON] [{now}] Обновляем периодические расходы...")

    expenses = (
        db_sess.query(Expense)
        .filter(
            Expense.periodicity.isnot(None),
            Expense.next_payment_date <= now,
        )
        .all()
    )

    for exp in expenses:
        print(
            f"[CRON] [{now}] Обновляем периодический расход: {exp.title} (id={exp.id}) (periodicity={exp.periodicity})"
        )

        new_exp_periodicity = exp.periodicity
        exp.periodicity = None
        exp.next_payment_date = None
        db_sess.add(exp)

        new_exp = Expense(
            group_id=exp.group_id,
            category_id=exp.category_id,
            title=exp.title,
            amount=exp.amount,
            currency=exp.currency,
            expense_type=exp.expense_type,
            split_type=exp.split_type,
            payment_method=exp.payment_method,
            periodicity=new_exp_periodicity,
            next_payment_date=now + timedelta(days=new_exp_periodicity),
            creation_date=now,
            is_paid=False,
        )
        db_sess.add(new_exp)

    db_sess.commit()
    db_sess.close()


def init_scheduler(app):
    scheduler.init_app(app)
    scheduler.start()

    scheduler.add_job(
        id="check_periodic_expenses_job",
        func=check_periodic_expenses,
        trigger="interval",
        minutes=app.config.get("CRON_RUN_COOLDOWN"),
    )

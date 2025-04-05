from datetime import datetime

from app.models import InvestmentBaseModel


def perform_investment(
    target: InvestmentBaseModel,
    sources: list[InvestmentBaseModel]
) -> list[InvestmentBaseModel]:
    changed = []
    for source in sources:
        new_invest_amount = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount
        )
        for obj in (target, source):
            obj.invested_amount += new_invest_amount
            if obj.invested_amount == obj.full_amount:
                obj.fully_invested = True
                obj.close_date = datetime.now()
        changed.append(source)
        if target.fully_invested:
            break
    return changed

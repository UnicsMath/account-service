from repository.account.iaccount_repository import (
    IAccountRepository,
    Session,
    AccountModel,
)


class AccountRepository(IAccountRepository):
    def get_by_email(self, db: Session, email: str) -> AccountModel:
        return db.query(AccountModel).filter(AccountModel.email == email).first()

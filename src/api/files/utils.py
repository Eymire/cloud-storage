from src.enums import UserSubscribePlan


subscribe_plan_to_storage_limit: dict[UserSubscribePlan, int] = {
    UserSubscribePlan.BASIC: 100 * 1024 * 1024,  # 100 MB
    UserSubscribePlan.PLUS: 200 * 1024 * 1024,  # 200 MB
    UserSubscribePlan.PRO: 500 * 1024 * 1024,  # 500 MB
}

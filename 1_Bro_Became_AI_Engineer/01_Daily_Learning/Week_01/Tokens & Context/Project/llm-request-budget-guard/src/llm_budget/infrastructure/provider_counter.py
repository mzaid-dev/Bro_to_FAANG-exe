from llm_budget.ports.token_counter import TokenCounter


class MockTokenCounter(TokenCounter):
    def count(self, text: str) -> int:
        """
        Temporary implementation.

        Assumes:
            1 token ≈ 4 characters

        This is ONLY for Day 1 learning.
        """

        return max(1, len(text) // 4)
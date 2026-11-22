from __future__ import annotations

from django.test import SimpleTestCase

from role_reward.progression import required_distinct_balls


class RequiredDistinctBallsTests(SimpleTestCase):
    def test_rounds_up_to_at_least_one_ball(self) -> None:
        self.assertEqual(required_distinct_balls(100, 0.005), 1)
        self.assertEqual(required_distinct_balls(101, 0.5), 51)

    def test_full_progression_requires_every_ball(self) -> None:
        self.assertEqual(required_distinct_balls(42, 1.0), 42)

    def test_rejects_invalid_inputs(self) -> None:
        for progression in (0, -0.1, 1.1):
            with self.subTest(progression=progression):
                with self.assertRaisesRegex(ValueError, "Progression"):
                    required_distinct_balls(100, progression)

        with self.assertRaisesRegex(ValueError, "cannot be negative"):
            required_distinct_balls(-1, 0.5)

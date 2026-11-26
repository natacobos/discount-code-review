# Review a pull request: discount codes at checkout

You are the technical lead of an online store's team. Sam, a junior developer who joined four months ago,
opened a pull request that lets customers type a discount code at checkout (for example `SUMMER15` for 15% off).

The change is two files:

- `pr/api/DiscountsController.cs`: the C# / .NET API endpoint.
- `pr/web/ApplyDiscount.jsx`: the React component on the checkout page.

Nothing to install or run: this is a code review.

You may use your usual AI tool; we will watch how you use it. Please think out loud.

## Your task: 8 minutes

The change has **6 problems** that should be fixed before it is merged. Each file has at least 2.
Find as many as you can and write your review in `REVIEW.md`, **one comment per line**, as you would
post it on Sam's pull request:

```
- DiscountsController.cs:12 What is wrong, why it matters, and what Sam should do instead.
```

Start each comment with the file name and the line number (or lines, like `:12-14`).
Write to Sam as you really would: he will read every comment.

If one problem takes you more than 2 minutes, write what you have and move on.

At 8 minutes we stop. Then run:

```
python3 check/check.py
```

Do not edit the files in `pr/` or the `check` folder.

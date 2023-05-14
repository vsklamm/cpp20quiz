## Thanks for helping!

Thank you for helping to port this question from C++17 to C++20.

## How to

Review and/or update the following files (tick after review even if it remains unchanged)

- [ ] Check if the correct answer for a question has changed or not: [link to Compiler Explorer](@@compiler_explorer_link@@) with source code of the current question and all needed compilers' settings.

* `explanation.md`
    - [ ] Refer to the correct section numbers: [C++20 standard draft](https://timsong-cpp.github.io/cppwp/std20/).

    @@c++17_standard_refs@@

    - [ ] Use updated quotes from those sections (the wording might have changed)
    - [ ] Make sure the rest of the text in the explanation is consistent with the new standard
    - [ ] Use proper markdown syntax: "quote" text from standard, "monospace" text related to code, etc. Good example: [question 313](/questions/313/explanation.md)
    - [ ] Pass through spell checker: [Grammarly](https://www.grammarly.com/), [ChatGPT](https://chat.openai.com/)      

* `hint.md` (Usually no need to update)
    - [ ] Make sure the text in the hint is consistent with the new standard
    - [ ] Pass through spell checker: [Grammarly](https://www.grammarly.com/), [ChatGPT](https://chat.openai.com/)


* `meta_data.json` (Only if the correct answer for a question has changed)

    The fields you need to care about are `answer` and `result`:

    - [ ] `answer`: If the program is supposed to compile and output something, put that output here. If not, set it to `""`.
    - [ ] `result`: Here you need to set the correct shorthand for an enum. The possible values are:
        * `OK`: The program is guaranteed a certain output
        * `CE`: The program has a compilation error
        * `US`: The program is unspecified / implementation defined
        * `UD`: The program has undefined behavior

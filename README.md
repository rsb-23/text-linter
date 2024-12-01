# actions/check-typo

This Github Action uses AI to find typos and grammatical errors in PR changes.

## Usage
Refer [test.yml](./.github/workflows/test.yml)
```yaml
  - name: Check typos in data files
    uses: actions/check-diff-typo@v1
    with:
      token: ${{ secrets.PAT }}
      files: |
        tests/file.txt
        tests/file.json
      GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
```

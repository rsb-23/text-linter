# Text Linter CI

This Github Action uses AI to find typos and grammatical errors in specified data files.

## Usage

Refer [test.yml](./.github/workflows/test.yml)

```yaml
  - name: Lint Text in Data Files
    uses: actions/text-linter@v1
    with:
      token: ${{ secrets.PAT }}
      files: |
        tests/file.txt
        tests/file.json
      provider: groq
      api_key: ${{ secrets.GROQ_API_KEY }}
      model:  //optional
```

## Supported Models & Providers

All text models supported by [Litellm](https://docs.litellm.ai/docs/providers).  
Hence `provider` name should be same as given in this doc.

# Instead of this:
response = model.generate(input_ids, max_length=1024)

# Do this:
response = model.generate(
    input_ids,
    max_new_tokens=512,  # Adjust this number based on your needs
    pad_token_id=tokenizer.eos_token_id
) 
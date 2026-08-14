export function getValidationErrorMessage(error: { issues?: Array<{ message?: string }> }) {
  return error.issues?.[0]?.message || "invalid payload";
}

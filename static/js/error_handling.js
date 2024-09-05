function handleError(error, context) {
    console.error(`Error in ${context}:`, error);
    showNotification(`An error occurred in ${context}. Please try again later.`, 'error');
}

function safelyExecuteFunction(func, context) {
    try {
        return func();
    } catch (error) {
        handleError(error, context);
    }
}
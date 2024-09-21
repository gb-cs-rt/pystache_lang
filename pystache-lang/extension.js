// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = require('vscode');

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {

	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	console.log('Congratulations, your extension "pystache-lang" is now active!');

	// The command has been defined in the package.json file
	// Now provide the implementation of the command with  registerCommand
	// The commandId parameter must match the command field in package.json
	const disposable = vscode.commands.registerCommand('pystache-lang.runFile', function () {
		// This should identify the path of the current file in the editor and run "pystache <file_path>" in the terminal

		// Get the active text editor
		const editor = vscode.window.activeTextEditor;
		if (!editor) {
			vscode.window.showInformationMessage('No active text editor found');
			return;
		}

		// Get the document object from the editor
		const document = editor.document;
		if (!document) {
			vscode.window.showInformationMessage('No document found');
			return;
		}

		// Get the file path of the document
		const filePath = document.fileName;
		if (!filePath) {
			vscode.window.showInformationMessage('No file path found');
			return;
		}

		// Run the command in the terminal (only create terminal if one does not exist)
		const terminal = vscode.window.terminals.find(terminal => terminal.name === 'Pystache');
		if (terminal) {
			terminal.show();
			terminal.sendText(`pystache ${filePath}`);
		} else {
			const newTerminal = vscode.window.createTerminal('Pystache');
			newTerminal.sendText(`pystache ${filePath}`);
			newTerminal.show();
		}
	});

	context.subscriptions.push(disposable);
}

// This method is called when your extension is deactivated
function deactivate() {}

module.exports = {
	activate,
	deactivate
}

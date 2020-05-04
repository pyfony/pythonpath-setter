import * as vscode from 'vscode';
var path = require('path');

function resolveNewPythonPath(): string {
	const config = vscode.workspace.getConfiguration('pythonPathSetter');
	let sourceDirs: Array<string> = config.sourceDirs
	let newPythonPath: string = sourceDirs.join(path.delimiter) + path.delimiter

	if (process.env.PYTHONPATH) {
		newPythonPath += process.env.PYTHONPATH;
	}

	return newPythonPath
}

export function activate(context: vscode.ExtensionContext) {
	context.subscriptions.push(vscode.debug.registerDebugConfigurationProvider('*', {
		resolveDebugConfiguration(folder: vscode.WorkspaceFolder | undefined, debugConfiguration: vscode.DebugConfiguration) {
			debugConfiguration.env['PYTHONPATH'] = resolveNewPythonPath();

			return debugConfiguration;
		}
	}));

	process.env['PYTHONPATH'] = resolveNewPythonPath();
}

export function deactivate() {}

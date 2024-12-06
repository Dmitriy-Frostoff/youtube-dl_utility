import { $, ExecaError } from 'execa';

/**
 * Updates python libs.
 * Note: npm update exitCode 0 => no updates, exitCode 1 => updates are available.
 *
 * @param {(pathToLogFile: string, error: Error | ExecaError) => Promise<void>} writeErrorLogFile - callback for
 *    async writing log file via NodeJS
 * @param {string} logFile - resolved via NodeJS path to the logfile
 * @returns {Promise<void>}
 */
export default async function updateNpmPackages(writeErrorLogFile, logFile) {
  try {
    console.log(
      'Outdated libs found. Running pip install -r requirements.txt --upgrade...\n',
    );
    await $(`pip install -r requirements.txt --upgrade`, {
      stdio: ['pipe', 'pipe', 'pipe'],
      cleanup: true,
    });
  } catch (error) {
    console.error(`An error occured: ${error.message}`);

    // write logfile beside the script
    await writeErrorLogFile(logFile, error);
  }
}

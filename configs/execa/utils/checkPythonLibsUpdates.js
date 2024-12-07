import { $, ExecaError } from 'execa';

/**
 * Check for outdated npm packages.
 * If there's now updates just write log file with date and 'No errors logged.' message and returns false.
 * If updates avalibale returns true.
 *
 * @param {(pathToLogFile: string, logMessage: string) => Promise<void>} writeSuccessLogFile - callback for
 *    async writing log file via NodeJS
 * @param {(pathToLogFile: string, error: Error | ExecaError) => Promise<void>} writeErrorLogFile - callback for
 *    async writing log file via NodeJS
 * @param {string} logFile - resolved via NodeJS path to the logfile
 * @returns {Promise<boolean | undefined>}
 */
export default async function checkPythonLibsUpdates(
  writeSuccessLogFile,
  writeErrorLogFile,
  logFile,
) {
  try {
    // { verbose: 'short' } => to show details in the terminal (use verbose: 'full' for all details)
    /** @type {import('execa').Result} */
    const { stdout } = await $(`pip list --outdated --format=json`, {
      stdio: ['pipe', 'pipe', 'pipe'],
      verbose: 'full',
      cleanup: true,
    });

    // stdout empty (i.e. []) (no updates) => return
    if (!stdout) {
      console.log('No outdated libs found.\n');

      // write logfile beside the script
      await writeSuccessLogFile(logFile, 'No outdated libs found.\n');
      return false;
    }

    /**
     * @type {Record<string, Record<string, string>>}
     * @example
     *    {
     *      "name": "charset-normalizer",
     *      "version": "3.3.2",
     *      "latest_version": "3.4.0",
     *      "latest_filetype": "wheel"
     *    },
     */
    const outdatedLibs = JSON.parse(stdout);

    // check that libs' list of updates is empty or that current && latest_version versions are the same
    if (
      Object.values(outdatedLibs).every(
        (lib) => lib.version === lib.latest_version,
      )
    ) {
      console.log(
        'All libs are up-to-date. Skipping pip install -r requirements.txt --upgrade',
      );
      // write logfile beside the script
      await writeSuccessLogFile(
        logFile,
        `All libs are up-to-date. Skipping pip install -r requirements.txt --upgrade\nstdout: ${stdout}`,
      );
      return false;
    }

    return true;
  } catch (error) {
    console.error(`An error occured: ${error.message}`);

    // write logfile beside the script
    await writeErrorLogFile(logFile, error);
  }
}

import { Component } from '@angular/core';
import { BackupService } from '../../services/backup.service';

@Component({
  selector: 'app-backup',
  templateUrl: './backup.component.html'
})
export class BackupComponent {
  isLoading = false;
  message = '';
  error = '';

  constructor(private backupService: BackupService) { }

  onBackup() {
    this.isLoading = true;
    this.message = '';
    this.error = '';

    this.backupService.backupDatabase().subscribe(
      (res: any) => {
        this.isLoading = false;
        if (res.message) {
          this.message = `Backup successful! File: ${res.backup_file}`;
        } else {
          this.error = 'Backup failed: ' + res.error;
        }
      },
      (err) => {
        this.isLoading = false;
        this.error = 'An error occurred during backup: ' + err.message;
      }
    );
  }
}

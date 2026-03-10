import { Component } from '@angular/core';
import { BackupService } from '../../services/backup.service';

@Component({
  selector: 'app-backup',
  templateUrl: './backup.component.html',
})
export class BackupComponent {
  message = '';
  isLoading = false;
  isError = false;

  constructor(private backupService: BackupService) {}

  createBackup() {
    this.isLoading = true;
    this.message = '';
    this.isError = false;

    this.backupService.backupDatabase().subscribe({
      next: (res: any) => {
        this.isLoading = false;
        if (res.error) {
          this.isError = true;
          this.message = 'Backup failed: ' + res.error;
        } else {
          this.message = 'Backup successful! File: ' + res.backup_file;
        }
      },
      error: (err: any) => {
        this.isLoading = false;
        this.isError = true;
        this.message = 'Backup failed: ' + (err.message || 'Unknown error');
      },
    });
  }
}

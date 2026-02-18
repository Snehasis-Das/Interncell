from alembic import op
import sqlalchemy as sa


revision = 'c4461d88ba90'
down_revision = '5b6b353af162'
branch_labels = None
depends_on = None


def upgrade() -> None:

    bind = op.get_bind()

    # --- Create ENUM types FIRST ---

    internship_work_mode = sa.Enum(
        'remote',
        'onsite',
        'hybrid',
        name='internship_work_mode'
    )
    internship_work_mode.create(bind, checkfirst=True)

    internship_timing = sa.Enum(
        'full_time',
        'part_time',
        name='internship_timing'
    )
    internship_timing.create(bind, checkfirst=True)

    internship_status = sa.Enum(
        'open',
        'closed',
        name='internship_status'
    )
    internship_status.create(bind, checkfirst=True)

    # --- Add new columns ---

    op.add_column('internships', sa.Column('details', sa.Text(), nullable=True))
    op.add_column('internships', sa.Column('location', sa.String(length=255), nullable=True))
    op.add_column('internships', sa.Column('work_mode', internship_work_mode, nullable=True))
    op.add_column('internships', sa.Column('timing', internship_timing, nullable=True))
    op.add_column('internships', sa.Column('experience_min_years', sa.Integer(), nullable=True))
    op.add_column('internships', sa.Column('duration_weeks', sa.Integer(), nullable=True))
    op.add_column('internships', sa.Column('stipend_amount', sa.Integer(), nullable=True))
    op.add_column('internships', sa.Column('stipend_currency', sa.String(length=10), nullable=True))
    op.add_column('internships', sa.Column('application_deadline', sa.DateTime(timezone=True), nullable=True))

    # --- Convert status column to ENUM ---
    op.execute(
        "ALTER TABLE internships "
        "ALTER COLUMN status TYPE internship_status "
        "USING status::internship_status"
    )


def downgrade() -> None:

    bind = op.get_bind()

    # --- Convert status back to VARCHAR ---
    op.execute(
        "ALTER TABLE internships "
        "ALTER COLUMN status TYPE VARCHAR(50)"
    )


    # --- Drop columns ---
    op.drop_column('internships', 'application_deadline')
    op.drop_column('internships', 'stipend_currency')
    op.drop_column('internships', 'stipend_amount')
    op.drop_column('internships', 'duration_weeks')
    op.drop_column('internships', 'experience_min_years')
    op.drop_column('internships', 'timing')
    op.drop_column('internships', 'work_mode')
    op.drop_column('internships', 'location')
    op.drop_column('internships', 'details')

    # --- Drop ENUM types LAST ---
    sa.Enum(name='internship_status').drop(bind, checkfirst=True)
    sa.Enum(name='internship_timing').drop(bind, checkfirst=True)
    sa.Enum(name='internship_work_mode').drop(bind, checkfirst=True)
